//! VK 寫的 TOML 檔（ADR-0008、ADR-0014）。
//!
//! - 讀取門檻只看根層的 `schema`（檔案版）：高於本引擎上限就回 [`ReadError::TooNew`]（VK0008），
//!   在讀任何已知欄位之前判定。`written_by` 只供回報，填進 VK0008 的 `<written_by>`，不影響讀取。
//! - 讀時忽略未知欄位、寫時保留：文件一律留在 `toml_edit` 的文件樹裡改，不先解成只含已知欄位的
//!   struct 再重建整份檔。改動只能經 [`Document::set`]、[`Document::remove`]，以及根層陣列表
//!   （例如 metadata 的 `[[file]]`）用的 [`Document::push_table`]、[`Document::set_in`]、
//!   [`Document::remove_in`]。
//! - 保留不了就拒絕寫，不悄悄少寫：會蓋掉表或陣列表的 `set` 直接回錯；[`Document::render`]
//!   輸出前再比對一次，讀進來時的每個值，凡是沒被明確改動的，輸出裡都得原樣還在，否則回錯；
//!   空的標準表只要求表還在，往裡面加鍵不算少寫。
//! - 這裡不讀寫檔案；輸入是檔案內容，輸出是要寫回的字串，原子寫入交給呼叫端。

use std::collections::BTreeMap;
use std::fmt;

use compat::Compat;
use messages::Message;
use toml_edit::{ArrayOfTables, DocumentMut, Item, Table, Value};

/// 檔案版欄位的鍵。
pub const SCHEMA_KEY: &str = "schema";
/// 寫入者欄位的鍵。
pub const WRITTEN_BY_KEY: &str = "written_by";

/// 一份已通過讀取門檻的 VK TOML。
#[derive(Debug, Clone)]
pub struct Document {
    doc: DocumentMut,
    schema: u32,
    written_by: Option<String>,
    /// 讀進來時每個值的路徑與正規化後的內容，給 [`Document::render`] 比對有沒有少寫。
    original: BTreeMap<Vec<Seg>, String>,
    /// 經 `set`／`remove`／`set_in`／`remove_in` 明確改過的路徑；這些路徑底下的值不必原樣保留。
    touched: Vec<Vec<Seg>>,
}

impl Document {
    /// 以本引擎（[`compat::THIS`]）的上限解析。
    pub fn parse(text: &str) -> Result<Document, ReadError> {
        Document::parse_with(text, &compat::THIS)
    }

    /// 以指定引擎的上限解析：先過 TOML 語法，再看 `schema`，通過門檻才回文件。
    pub fn parse_with(text: &str, engine: &Compat) -> Result<Document, ReadError> {
        let doc: DocumentMut = text
            .parse()
            .map_err(|e: toml_edit::TomlError| ReadError::Syntax(e.message().to_owned()))?;
        let written_by = doc
            .get(WRITTEN_BY_KEY)
            .and_then(Item::as_str)
            .map(str::to_owned);
        let schema = match doc.get(SCHEMA_KEY) {
            None | Some(Item::None) => return Err(ReadError::MissingSchema),
            Some(item) => item
                .as_integer()
                .and_then(|n| u32::try_from(n).ok())
                .filter(|n| *n >= 1)
                .ok_or_else(|| ReadError::BadSchema(item.to_string().trim().to_owned()))?,
        };
        engine.check_schema(schema).map_err(|too_new| {
            ReadError::TooNew(TooNew {
                too_new,
                written_by: written_by.clone(),
            })
        })?;
        let mut original = BTreeMap::new();
        collect_table(doc.as_table(), &mut Vec::new(), &mut original);
        Ok(Document {
            doc,
            schema,
            written_by,
            original,
            touched: Vec::new(),
        })
    }

    /// 新檔：只有本引擎的檔案版與空的寫入者，寫入者在 [`Document::render`] 時填上。
    pub fn new() -> Document {
        let mut doc = DocumentMut::new();
        doc.insert(
            SCHEMA_KEY,
            toml_edit::value(i64::from(compat::THIS.max_schema)),
        );
        doc.insert(WRITTEN_BY_KEY, toml_edit::value(""));
        Document {
            doc,
            schema: compat::THIS.max_schema,
            written_by: None,
            original: BTreeMap::new(),
            touched: Vec::new(),
        }
    }

    /// 檔案版。
    pub fn schema(&self) -> u32 {
        self.schema
    }

    /// 讀進來時的寫入者；欄位不在或不是字串時是 `None`。只供回報。
    pub fn written_by(&self) -> Option<&str> {
        self.written_by.as_deref()
    }

    /// 依路徑取值；只走標準表，路徑不在就是 `None`。未知欄位不必理會，留在文件裡即可。
    pub fn get(&self, path: &[&str]) -> Option<&Item> {
        let (last, parents) = path.split_last()?;
        let mut table = self.doc.as_table();
        for key in parents {
            table = table.get(key)?.as_table()?;
        }
        table.get(last)
    }

    /// 根表，給呼叫端唯讀走訪。
    pub fn root(&self) -> &Table {
        self.doc.as_table()
    }

    /// 設定一個值。中間缺的表會建成隱式表；原本是一般值就換掉並保留它前後的空白與註解。
    /// 中間不是標準表、或原本是表、陣列表、inline table 時回錯，文件不變：
    /// 換掉它們會連帶丟掉裡面的未知欄位。
    pub fn set(&mut self, path: &[&str], value: impl Into<Value>) -> Result<(), WriteError> {
        let (last, parents) = path.split_last().ok_or(WriteError::EmptyPath)?;
        // 先確認整條路徑可寫，再動文件，失敗時不留下半途建的表。
        let mut probe = Some(self.doc.as_table());
        for (i, key) in parents.iter().enumerate() {
            probe = match probe.and_then(|t| t.get(key)) {
                None | Some(Item::None) => None,
                Some(Item::Table(t)) => Some(t),
                Some(_) => {
                    return Err(WriteError::NotATable {
                        path: join(&path[..=i]),
                    });
                }
            };
        }
        if let Some(existing) = probe.and_then(|t| t.get(last)) {
            match existing {
                Item::None => {}
                Item::Value(v) if !matches!(v, Value::InlineTable(_)) => {}
                _ => {
                    return Err(WriteError::WouldClobber { path: join(path) });
                }
            }
        }

        let mut table = self.doc.as_table_mut();
        for key in parents {
            let item = table.entry(key).or_insert_with(implicit_table);
            table = match item {
                Item::Table(t) => t,
                _ => return Err(WriteError::NotATable { path: join(path) }),
            };
        }
        let mut value = value.into();
        match table.get_mut(last) {
            Some(Item::Value(old)) => {
                *value.decor_mut() = old.decor().clone();
                *old = value;
            }
            _ => {
                table.insert(last, Item::Value(value));
            }
        }
        self.touched.push(key_path(path));
        Ok(())
    }

    /// 明確刪掉一個鍵（連同它底下的全部內容），回傳被刪的項；路徑不在回 `None`。
    pub fn remove(&mut self, path: &[&str]) -> Result<Option<Item>, WriteError> {
        let (last, parents) = path.split_last().ok_or(WriteError::EmptyPath)?;
        let mut table = self.doc.as_table_mut();
        for (i, key) in parents.iter().enumerate() {
            table = match table.get_mut(key) {
                None | Some(Item::None) => return Ok(None),
                Some(Item::Table(t)) => t,
                Some(_) => {
                    return Err(WriteError::NotATable {
                        path: join(&path[..=i]),
                    });
                }
            };
        }
        let removed = table.remove(last);
        if removed.is_some() {
            self.touched.push(key_path(path));
        }
        Ok(removed)
    }

    /// 根層陣列表 `array` 的表數；鍵不在時是 0，不是陣列表時回錯。
    pub fn table_count(&self, array: &str) -> Result<usize, WriteError> {
        match self.doc.as_table().get(array) {
            None | Some(Item::None) => Ok(0),
            Some(Item::ArrayOfTables(a)) => Ok(a.len()),
            Some(_) => Err(WriteError::NotAnArrayOfTables {
                path: array.to_owned(),
            }),
        }
    }

    /// 在根層陣列表 `array` 的最後加一個空表，回傳它的索引；鍵不在時建出陣列表。
    /// 鍵原本是別種值時回錯，文件不變。
    pub fn push_table(&mut self, array: &str) -> Result<usize, WriteError> {
        let root = self.doc.as_table_mut();
        match root.get_mut(array) {
            None | Some(Item::None) => {
                let mut tables = ArrayOfTables::new();
                tables.push(Table::new());
                root.insert(array, Item::ArrayOfTables(tables));
                Ok(0)
            }
            Some(Item::ArrayOfTables(a)) => {
                a.push(Table::new());
                Ok(a.len() - 1)
            }
            Some(_) => Err(WriteError::NotAnArrayOfTables {
                path: array.to_owned(),
            }),
        }
    }

    /// 在根層陣列表 `array` 的第 `index` 個表裡設定 `key`。規則同 [`Document::set`]：
    /// 原本是一般值就換掉並保留前後的空白與註解；原本是表、陣列表或 inline table 時回錯。
    /// 同一個表裡的其他欄位與其他表都不受影響。
    pub fn set_in(
        &mut self,
        array: &str,
        index: usize,
        key: &str,
        value: impl Into<Value>,
    ) -> Result<(), WriteError> {
        let path = indexed_path(array, index, key);
        let table = self.array_table_mut(array, index)?;
        let mut value = value.into();
        match table.get_mut(key) {
            None | Some(Item::None) => {
                table.insert(key, Item::Value(value));
            }
            Some(Item::Value(old)) if !matches!(old, Value::InlineTable(_)) => {
                *value.decor_mut() = old.decor().clone();
                *old = value;
            }
            Some(_) => {
                return Err(WriteError::WouldClobber {
                    path: render_path(&path),
                });
            }
        }
        self.touched.push(path);
        Ok(())
    }

    /// 明確刪掉根層陣列表 `array` 第 `index` 個表裡的 `key`，回傳被刪的項；鍵不在回 `None`。
    pub fn remove_in(
        &mut self,
        array: &str,
        index: usize,
        key: &str,
    ) -> Result<Option<Item>, WriteError> {
        let path = indexed_path(array, index, key);
        let removed = self.array_table_mut(array, index)?.remove(key);
        if removed.is_some() {
            self.touched.push(path);
        }
        Ok(removed)
    }

    fn array_table_mut(&mut self, array: &str, index: usize) -> Result<&mut Table, WriteError> {
        match self.doc.as_table_mut().get_mut(array) {
            Some(Item::ArrayOfTables(a)) => {
                a.get_mut(index).ok_or_else(|| WriteError::NoSuchTable {
                    path: render_path(&[Seg::Key(array.to_owned()), Seg::Index(index)]),
                })
            }
            None | Some(Item::None) => Err(WriteError::NoSuchTable {
                path: render_path(&[Seg::Key(array.to_owned()), Seg::Index(index)]),
            }),
            Some(_) => Err(WriteError::NotAnArrayOfTables {
                path: array.to_owned(),
            }),
        }
    }

    /// 蓋上檔案版與寫入者，確認沒有少寫後回傳要寫回的內容。
    /// 檔案版沿用讀進來的值，跨檔案版的遷移不在這裡做。
    pub fn render(&mut self, written_by: &str) -> Result<String, WriteError> {
        self.set(&[SCHEMA_KEY], i64::from(self.schema))?;
        self.set(&[WRITTEN_BY_KEY], written_by)?;
        self.check_nothing_dropped()?;
        Ok(self.doc.to_string())
    }

    /// 讀進來時的每個值，沒被明確改動的，現在都得原樣還在。
    fn check_nothing_dropped(&self) -> Result<(), WriteError> {
        let mut now = BTreeMap::new();
        collect_table(self.doc.as_table(), &mut Vec::new(), &mut now);
        let dropped: Vec<String> = self
            .original
            .iter()
            .filter(|(path, _)| !self.is_touched(path))
            .filter(|(path, repr)| !kept(&now, path, repr))
            .map(|(path, _)| render_path(path))
            .collect();
        if dropped.is_empty() {
            Ok(())
        } else {
            Err(WriteError::WouldDrop { paths: dropped })
        }
    }

    fn is_touched(&self, path: &[Seg]) -> bool {
        self.touched
            .iter()
            .any(|t| t.len() <= path.len() && t[..] == path[..t.len()])
    }
}

impl Default for Document {
    fn default() -> Self {
        Document::new()
    }
}

/// 讀取失敗。
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ReadError {
    /// 不是合法的 TOML。
    Syntax(String),
    /// 根層沒有 `schema`。
    MissingSchema,
    /// `schema` 不是正整數；帶著原本的值。
    BadSchema(String),
    /// 檔案版高於本引擎上限（VK0008）。
    TooNew(TooNew),
}

impl ReadError {
    /// 對應的訊息表條目。只有檔案版過高有代碼；語法錯與 `schema` 缺漏或不合，
    /// 訊息表還沒有代碼（計畫缺口 G3 一類），先回 `None`。
    pub fn message(&self) -> Option<&'static Message> {
        match self {
            ReadError::TooNew(e) => Some(e.message()),
            _ => None,
        }
    }
}

impl fmt::Display for ReadError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            ReadError::Syntax(m) => write!(f, "invalid TOML: {m}"),
            ReadError::MissingSchema => write!(f, "missing `{SCHEMA_KEY}`"),
            ReadError::BadSchema(v) => write!(f, "`{SCHEMA_KEY}` is not a positive integer: {v}"),
            ReadError::TooNew(e) => e.fmt(f),
        }
    }
}

impl std::error::Error for ReadError {}

/// 檔案版過高（VK0008），帶著填訊息用的值；`<file>` 由讀檔的一方填。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct TooNew {
    too_new: compat::SchemaTooNew,
    written_by: Option<String>,
}

impl TooNew {
    /// 對應的訊息表條目（VK0008）。
    pub fn message(&self) -> &'static Message {
        self.too_new.message()
    }

    /// 檔裡的檔案版，填 `<N>`。
    pub fn found(&self) -> u32 {
        self.too_new.found
    }

    /// 本引擎的上限，填 `<M>`。
    pub fn max(&self) -> u32 {
        self.too_new.max
    }

    /// 檔裡記的寫入者，填 `<written_by>`；欄位不在或不是字串時是 `None`。
    pub fn written_by(&self) -> Option<&str> {
        self.written_by.as_deref()
    }
}

impl fmt::Display for TooNew {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        self.too_new.fmt(f)?;
        if let Some(w) = &self.written_by {
            write!(f, "; written by vendor_kit {w}")?;
        }
        Ok(())
    }
}

/// 拒絕寫入：照做會少寫或蓋掉保留不了的內容。
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum WriteError {
    /// 路徑是空的。
    EmptyPath,
    /// 路徑中途不是標準表（一般值、inline table 或陣列表）。
    NotATable { path: String },
    /// 目標原本是表、陣列表或 inline table，換掉會丟掉裡面的內容。
    WouldClobber { path: String },
    /// 輸出前比對發現少了這些原本的值。
    WouldDrop { paths: Vec<String> },
    /// 根層的這個鍵不是陣列表。
    NotAnArrayOfTables { path: String },
    /// 陣列表裡沒有這個索引的表。
    NoSuchTable { path: String },
}

impl fmt::Display for WriteError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            WriteError::EmptyPath => write!(f, "empty key path"),
            WriteError::NotATable { path } => write!(f, "`{path}` is not a standard table"),
            WriteError::WouldClobber { path } => {
                write!(f, "refusing to replace table-like value at `{path}`")
            }
            WriteError::WouldDrop { paths } => {
                write!(f, "refusing to write: would drop {}", paths.join(", "))
            }
            WriteError::NotAnArrayOfTables { path } => {
                write!(f, "`{path}` is not an array of tables")
            }
            WriteError::NoSuchTable { path } => write!(f, "no table at `{path}`"),
        }
    }
}

impl std::error::Error for WriteError {}

/// 值在文件樹裡的位置：鍵或陣列表的索引。
#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord)]
enum Seg {
    Key(String),
    Index(usize),
}

fn implicit_table() -> Item {
    let mut t = Table::new();
    t.set_implicit(true);
    Item::Table(t)
}

fn key_path(path: &[&str]) -> Vec<Seg> {
    path.iter().map(|k| Seg::Key((*k).to_owned())).collect()
}

fn indexed_path(array: &str, index: usize, key: &str) -> Vec<Seg> {
    vec![
        Seg::Key(array.to_owned()),
        Seg::Index(index),
        Seg::Key(key.to_owned()),
    ]
}

fn join(path: &[&str]) -> String {
    path.join(".")
}

fn render_path(path: &[Seg]) -> String {
    let mut s = String::new();
    for seg in path {
        match seg {
            Seg::Key(k) => {
                if !s.is_empty() {
                    s.push('.');
                }
                s.push_str(k);
            }
            Seg::Index(i) => s.push_str(&format!("[{i}]")),
        }
    }
    s
}

/// 攤平成「路徑 → 正規化的值」；空表也記一筆，空的未知表一樣要保留。
/// 空的標準表的記號。跟 [`canonical`] 的輸出都不同，空的 inline table 仍是 `{}`。
const EMPTY_TABLE: &str = "<empty table>";

/// 讀進來時的 `path` 現在還在不在。空的標準表只要求表還在：之後往裡面加鍵
/// （例如 `undev` 留下空的 `[tools]` 後再 `dev`）不算少寫，表整個不見才算。
fn kept(now: &BTreeMap<Vec<Seg>, String>, path: &[Seg], repr: &str) -> bool {
    if now.get(path).map(String::as_str) == Some(repr) {
        return true;
    }
    repr == EMPTY_TABLE
        && now
            .range(path.to_vec()..)
            .take_while(|(p, _)| p.starts_with(path))
            .any(|(p, _)| p.len() > path.len())
}

fn collect_table(table: &Table, path: &mut Vec<Seg>, out: &mut BTreeMap<Vec<Seg>, String>) {
    if table.is_empty() && !path.is_empty() {
        out.insert(path.clone(), EMPTY_TABLE.to_owned());
    }
    for (key, item) in table.iter() {
        path.push(Seg::Key(key.to_owned()));
        collect_item(item, path, out);
        path.pop();
    }
}

fn collect_item(item: &Item, path: &mut Vec<Seg>, out: &mut BTreeMap<Vec<Seg>, String>) {
    match item {
        Item::None => {}
        Item::Value(v) => {
            out.insert(path.clone(), canonical(v));
        }
        Item::Table(t) => collect_table(t, path, out),
        Item::ArrayOfTables(a) => {
            for (i, t) in a.iter().enumerate() {
                path.push(Seg::Index(i));
                collect_table(t, path, out);
                path.pop();
            }
        }
    }
}

/// 值的內容，不含空白與註解；只用來比對有沒有變。
fn canonical(v: &Value) -> String {
    match v {
        Value::String(s) => format!("{:?}", s.value()),
        Value::Integer(i) => format!("i{}", i.value()),
        Value::Float(x) => format!("f{:x}", x.value().to_bits()),
        Value::Boolean(b) => format!("b{}", b.value()),
        Value::Datetime(d) => format!("d{}", d.value()),
        Value::Array(a) => {
            let items: Vec<String> = a.iter().map(canonical).collect();
            format!("[{}]", items.join(","))
        }
        Value::InlineTable(t) => {
            let mut items: Vec<String> = t
                .iter()
                .map(|(k, v)| format!("{k:?}={}", canonical(v)))
                .collect();
            items.sort();
            format!("{{{}}}", items.join(","))
        }
    }
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::expect_used)]
mod tests {
    use super::*;

    /// 有已知欄位、未知欄位、未知表、陣列表與各處註解的檔。
    const SAMPLE: &str = r#"# VK 寫的檔
schema = 1
written_by = "v0.1.0"
name = "demo"  # 已知欄位的註解
future_key = [1, 2, 3]

[extra]
# 新版才有的表
note = 'kept'
empty = {}

[[later]]
id = 1

[[later]]
id = 2
"#;

    #[test]
    fn untouched_document_round_trips_byte_for_byte() {
        let doc = Document::parse(SAMPLE).unwrap();
        assert_eq!(doc.doc.to_string(), SAMPLE);
        let mut doc = doc;
        assert_eq!(doc.render("v0.1.0").unwrap(), SAMPLE);
    }

    #[test]
    fn editing_known_field_keeps_unknown_fields_and_comments() {
        let mut doc = Document::parse(SAMPLE).unwrap();
        doc.set(&["name"], "renamed").unwrap();
        let out = doc.render("v0.2.0").unwrap();
        let expected = SAMPLE
            .replace(r#"name = "demo""#, r#"name = "renamed""#)
            .replace(r#"written_by = "v0.1.0""#, r#"written_by = "v0.2.0""#);
        assert_eq!(out, expected);
    }

    #[test]
    fn new_nested_key_goes_into_new_table_and_keeps_the_rest() {
        let mut doc = Document::parse(SAMPLE).unwrap();
        doc.set(&["tool", "ref"], "ghcr.io/o/r:v1.0.0").unwrap();
        let out = doc.render("v0.1.0").unwrap();
        assert!(out.starts_with(SAMPLE));
        let again = Document::parse(&out).unwrap();
        assert_eq!(
            again.get(&["tool", "ref"]).and_then(Item::as_str),
            Some("ghcr.io/o/r:v1.0.0")
        );
        assert_eq!(
            again.get(&["extra", "note"]).and_then(Item::as_str),
            Some("kept")
        );
    }

    #[test]
    fn reads_ignore_unknown_fields() {
        let doc = Document::parse(SAMPLE).unwrap();
        assert_eq!(doc.schema(), 1);
        assert_eq!(doc.written_by(), Some("v0.1.0"));
        assert_eq!(doc.get(&["name"]).and_then(Item::as_str), Some("demo"));
        assert!(doc.get(&["missing", "key"]).is_none());
    }

    #[test]
    fn schema_above_max_is_rejected_before_known_fields_with_vk0008() {
        // 已知欄位型別不對也不影響：先判檔案版。
        let text = "schema = 2\nwritten_by = \"v9.0.0\"\nname = 3\n";
        let err = Document::parse(text).unwrap_err();
        let ReadError::TooNew(e) = &err else {
            panic!("expected TooNew, got {err:?}");
        };
        assert_eq!(e.found(), 2);
        assert_eq!(e.max(), compat::THIS.max_schema);
        assert_eq!(e.written_by(), Some("v9.0.0"));
        assert_eq!(err.message().map(|m| m.code), Some("VK0008"));
        assert_eq!(e.message().exit_code(), 3);
    }

    #[test]
    fn written_by_is_only_reported() {
        let text = "schema = 1\nwritten_by = 42\n";
        let doc = Document::parse(text).unwrap();
        assert_eq!(doc.written_by(), None);

        let text = "schema = 2\nwritten_by = 42\n";
        let ReadError::TooNew(e) = Document::parse(text).unwrap_err() else {
            panic!("expected TooNew");
        };
        assert_eq!(e.written_by(), None);
    }

    #[test]
    fn engine_with_higher_max_reads_newer_schema() {
        let engine = Compat {
            max_schema: 2,
            ..compat::THIS
        };
        let doc = Document::parse_with("schema = 2\n", &engine).unwrap();
        assert_eq!(doc.schema(), 2);
    }

    #[test]
    fn missing_or_bad_schema_is_rejected_without_code() {
        assert_eq!(
            Document::parse("name = 1\n").unwrap_err(),
            ReadError::MissingSchema
        );
        for bad in [
            "schema = 0",
            "schema = -1",
            "schema = \"1\"",
            "schema = 1.0",
        ] {
            let err = Document::parse(bad).unwrap_err();
            assert!(matches!(err, ReadError::BadSchema(_)), "{bad}: {err:?}");
            assert_eq!(err.message(), None);
        }
        let err = Document::parse("schema = ").unwrap_err();
        assert!(matches!(err, ReadError::Syntax(_)));
    }

    #[test]
    fn set_refuses_to_clobber_and_leaves_document_unchanged() {
        let mut doc = Document::parse(SAMPLE).unwrap();
        assert_eq!(
            doc.set(&["name", "inner"], 1),
            Err(WriteError::NotATable {
                path: "name".to_owned()
            })
        );
        assert_eq!(
            doc.set(&["extra"], "x"),
            Err(WriteError::WouldClobber {
                path: "extra".to_owned()
            })
        );
        assert_eq!(
            doc.set(&["later"], 1),
            Err(WriteError::WouldClobber {
                path: "later".to_owned()
            })
        );
        assert_eq!(
            doc.set(&["extra", "empty"], 1),
            Err(WriteError::WouldClobber {
                path: "extra.empty".to_owned()
            })
        );
        assert_eq!(
            doc.set(&["later", "id"], 1),
            Err(WriteError::NotATable {
                path: "later".to_owned()
            })
        );
        assert_eq!(doc.set(&[], 1), Err(WriteError::EmptyPath));
        assert_eq!(doc.doc.to_string(), SAMPLE);
    }

    #[test]
    fn render_refuses_when_a_value_would_be_dropped() {
        let mut doc = Document::parse(SAMPLE).unwrap();
        // 模擬繞過 set／remove 的改動：未知欄位不見了。
        doc.doc["extra"]
            .as_table_mut()
            .unwrap()
            .remove("note")
            .unwrap();
        assert_eq!(
            doc.render("v0.1.0"),
            Err(WriteError::WouldDrop {
                paths: vec!["extra.note".to_owned()]
            })
        );
    }

    #[test]
    fn render_refuses_when_a_value_would_change() {
        let mut doc = Document::parse(SAMPLE).unwrap();
        doc.doc["later"].as_array_of_tables_mut().unwrap().remove(1);
        assert_eq!(
            doc.render("v0.1.0"),
            Err(WriteError::WouldDrop {
                paths: vec!["later[1].id".to_owned()]
            })
        );
    }

    #[test]
    fn keys_added_to_an_empty_table_are_not_a_drop() {
        // undev 解除最後一個覆寫後留下空的 [tools]，再 dev 往裡面加鍵。
        let mut doc = Document::parse("schema = 1\n\n[tools]\n\n[[later]]\n").unwrap();
        doc.set(&["tools", "tool"], "dev/tool").unwrap();
        doc.set_in("later", 0, "id", 1).unwrap();
        let out = doc.render("v0.1.0").unwrap();
        assert!(out.contains("tool = \"dev/tool\""), "{out}");
        assert!(out.contains("id = 1"), "{out}");
    }

    #[test]
    fn render_refuses_when_an_empty_table_would_be_dropped() {
        let mut doc = Document::parse("schema = 1\n\n[tools]\n\n[[later]]\n").unwrap();
        doc.doc.as_table_mut().remove("tools").unwrap();
        assert_eq!(
            doc.render("v0.1.0"),
            Err(WriteError::WouldDrop {
                paths: vec!["tools".to_owned()]
            })
        );
        // 空表換成值也不算還在；空的 inline table 照舊整個比對。
        let mut doc = Document::parse("schema = 1\nempty = {}\n\n[tools]\n").unwrap();
        doc.doc["tools"] = toml_edit::value("x");
        doc.doc["empty"] = toml_edit::value(toml_edit::InlineTable::from_iter([("k", 1)]));
        assert_eq!(
            doc.render("v0.1.0"),
            Err(WriteError::WouldDrop {
                paths: vec!["empty".to_owned(), "tools".to_owned()]
            })
        );
    }

    #[test]
    fn explicit_remove_is_allowed() {
        let mut doc = Document::parse(SAMPLE).unwrap();
        assert!(doc.remove(&["extra"]).unwrap().is_some());
        assert!(doc.remove(&["nope", "x"]).unwrap().is_none());
        let out = doc.render("v0.1.0").unwrap();
        assert!(!out.contains("[extra]"));
        assert!(out.contains("[[later]]"));
    }

    #[test]
    fn array_table_edits_keep_other_fields_and_tables() {
        let text = "schema = 1\nwritten_by = \"v0.1.0\"\n\n[[later]]\nid = 1 # one\nnote = \"keep\"\n\n[[later]]\nid = 2\nextra = 9\n";
        let mut doc = Document::parse(text).unwrap();
        assert_eq!(doc.table_count("later"), Ok(2));
        doc.set_in("later", 0, "id", 10).unwrap();
        assert!(doc.remove_in("later", 1, "extra").unwrap().is_some());
        assert!(doc.remove_in("later", 1, "nope").unwrap().is_none());
        let i = doc.push_table("later").unwrap();
        assert_eq!(i, 2);
        doc.set_in("later", i, "id", 3).unwrap();
        let out = doc.render("v0.2.0").unwrap();
        let again = Document::parse(&out).unwrap();
        let tables = again.get(&["later"]).unwrap().as_array_of_tables().unwrap();
        let ids: Vec<i64> = tables
            .iter()
            .map(|t| t["id"].as_integer().unwrap())
            .collect();
        assert_eq!(ids, [10, 2, 3]);
        assert!(out.contains("id = 10 # one"));
        assert!(out.contains("note = \"keep\""));
        assert!(!out.contains("extra"));
    }

    #[test]
    fn array_table_edits_do_not_excuse_other_entries() {
        let text = "schema = 1\n\n[[later]]\nid = 1\n\n[[later]]\nid = 2\nnote = \"x\"\n";
        let mut doc = Document::parse(text).unwrap();
        doc.set_in("later", 0, "id", 5).unwrap();
        // 繞過 API 拿掉第二個表的未知欄位：改過第一個表不代表第二個表可以少寫。
        doc.doc["later"]
            .as_array_of_tables_mut()
            .unwrap()
            .get_mut(1)
            .unwrap()
            .remove("note");
        assert_eq!(
            doc.render("v0.1.0"),
            Err(WriteError::WouldDrop {
                paths: vec!["later[1].note".to_owned()]
            })
        );
    }

    #[test]
    fn array_table_edits_refuse_bad_targets() {
        let mut doc = Document::parse(SAMPLE).unwrap();
        assert_eq!(
            doc.push_table("name"),
            Err(WriteError::NotAnArrayOfTables {
                path: "name".to_owned()
            })
        );
        assert_eq!(
            doc.set_in("later", 5, "id", 1),
            Err(WriteError::NoSuchTable {
                path: "later[5]".to_owned()
            })
        );
        assert_eq!(
            doc.set_in("missing", 0, "id", 1),
            Err(WriteError::NoSuchTable {
                path: "missing[0]".to_owned()
            })
        );
        assert_eq!(
            doc.table_count("extra"),
            Err(WriteError::NotAnArrayOfTables {
                path: "extra".to_owned()
            })
        );
        assert_eq!(doc.table_count("missing"), Ok(0));
        assert_eq!(doc.doc.to_string(), SAMPLE);
    }

    #[test]
    fn push_table_creates_the_array() {
        let mut doc = Document::new();
        let i = doc.push_table("file").unwrap();
        doc.set_in("file", i, "path", "a").unwrap();
        let out = doc.render("v0.1.0").unwrap();
        assert!(out.contains("[[file]]\npath = \"a\""), "{out}");
    }

    #[test]
    fn new_document_records_schema_and_writer() {
        let mut doc = Document::new();
        doc.set(&["name"], "demo").unwrap();
        let out = doc.render("v0.3.0").unwrap();
        let again = Document::parse(&out).unwrap();
        assert_eq!(again.schema(), compat::THIS.max_schema);
        assert_eq!(again.written_by(), Some("v0.3.0"));
        assert_eq!(again.get(&["name"]).and_then(Item::as_str), Some("demo"));
    }
}
