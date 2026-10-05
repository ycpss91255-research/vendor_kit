//! 讀 `.drawio`：`<mxfile>` 底下每個 `<diagram id>` 是一頁，頁裡每個 cell 以 cell id 為鍵。
//! 規則只比 id 與 style，不比中文標籤；value 去 HTML 後只用在錯誤訊息。

/// 紅框（VK 開發的元件）的 style 標記。
const RED_FRAME: &str = "strokeColor=#b85450";

/// 一個 cell。`<object>`／`<UserObject>` 包裝時，id 與標籤取自包裝，style 等取自內層 `<mxCell>`。
#[derive(Debug)]
pub struct Cell {
    pub id: String,
    /// 原始 value（或包裝的 label），可能含 HTML。
    pub value: String,
    pub style: String,
    pub parent: Option<String>,
    pub vertex: bool,
}

impl Cell {
    /// style 是否有這一項（`key=value`，以 `;` 分隔，不分大小寫）。
    pub fn style_has(&self, item: &str) -> bool {
        self.style
            .split(';')
            .any(|t| t.trim().eq_ignore_ascii_case(item))
    }

    /// 紅框：style 含 `strokeColor=#b85450` 的方塊（不含線）。
    pub fn is_red_frame(&self) -> bool {
        self.vertex && self.style_has(RED_FRAME)
    }

    /// 給錯誤訊息用的標籤：去 HTML、還原 entity。
    pub fn label(&self) -> String {
        plain_text(&self.value)
    }
}

/// 一頁：`<diagram id>` 與它的 cell（保持檔內順序）。
#[derive(Debug)]
pub struct Page {
    pub id: String,
    pub cells: Vec<Cell>,
}

impl Page {
    /// 這個 id 的所有 cell（正常只有一個）。
    pub fn cells_with_id<'a>(&'a self, id: &'a str) -> impl Iterator<Item = &'a Cell> + 'a {
        self.cells.iter().filter(move |c| c.id == id)
    }
}

/// 解析整份 `.drawio`。壓縮的頁直接報錯，不略過。
pub fn parse(xml: &str) -> Result<Vec<Page>, String> {
    let doc = roxmltree::Document::parse(xml).map_err(|e| format!("XML 解析失敗：{e}"))?;
    let root = doc.root_element();
    if root.tag_name().name() != "mxfile" {
        return Err(format!(
            "根元素是 <{}>，不是 <mxfile>",
            root.tag_name().name()
        ));
    }
    let mut pages: Vec<Page> = Vec::new();
    for diagram in root.children().filter(|n| n.has_tag_name("diagram")) {
        let id = diagram
            .attribute("id")
            .ok_or("有 <diagram> 沒有 id；頁一律以 <diagram id> 為鍵")?
            .to_owned();
        if pages.iter().any(|p| p.id == id) {
            return Err(format!("<diagram id=\"{id}\"> 重複"));
        }
        let Some(model) = diagram.children().find(|n| n.has_tag_name("mxGraphModel")) else {
            let has_text = diagram
                .children()
                .any(|n| n.is_text() && n.text().is_some_and(|t| !t.trim().is_empty()));
            return Err(if has_text {
                format!("頁 {id} 是壓縮格式，請存成未壓縮（drawio：檔案 > 屬性，取消「壓縮」）")
            } else {
                format!("頁 {id} 沒有 <mxGraphModel>")
            });
        };
        let graph_root = model
            .children()
            .find(|n| n.has_tag_name("root"))
            .ok_or_else(|| format!("頁 {id} 的 <mxGraphModel> 沒有 <root>"))?;
        let mut cells = Vec::new();
        for node in graph_root.children().filter(|n| n.is_element()) {
            let cell = match node.tag_name().name() {
                "mxCell" => Cell {
                    id: node.attribute("id").unwrap_or_default().to_owned(),
                    value: node.attribute("value").unwrap_or_default().to_owned(),
                    style: node.attribute("style").unwrap_or_default().to_owned(),
                    parent: node.attribute("parent").map(str::to_owned),
                    vertex: node.attribute("vertex") == Some("1"),
                },
                "object" | "UserObject" => {
                    let inner = node
                        .children()
                        .find(|n| n.has_tag_name("mxCell"))
                        .ok_or_else(|| {
                            format!("頁 {id} 的 <{}> 裡沒有 <mxCell>", node.tag_name().name())
                        })?;
                    Cell {
                        id: node.attribute("id").unwrap_or_default().to_owned(),
                        value: node
                            .attribute("label")
                            .or_else(|| node.attribute("value"))
                            .unwrap_or_default()
                            .to_owned(),
                        style: inner.attribute("style").unwrap_or_default().to_owned(),
                        parent: inner.attribute("parent").map(str::to_owned),
                        vertex: inner.attribute("vertex") == Some("1"),
                    }
                }
                _ => continue,
            };
            if cell.id.is_empty() {
                return Err(format!("頁 {id} 有沒有 id 的 cell"));
            }
            cells.push(cell);
        }
        pages.push(Page { id, cells });
    }
    Ok(pages)
}

/// 去 HTML 標籤、還原 entity、合併空白。
fn plain_text(html: &str) -> String {
    let mut out = String::new();
    let mut rest = html;
    while let Some(start) = rest.find('<') {
        out.push_str(&rest[..start]);
        match rest[start..].find('>') {
            Some(end) => {
                out.push(' ');
                rest = &rest[start + end + 1..];
            }
            None => {
                rest = &rest[start..];
                break;
            }
        }
    }
    out.push_str(rest);
    decode_entities(&out)
        .split_whitespace()
        .collect::<Vec<_>>()
        .join(" ")
}

fn decode_entities(s: &str) -> String {
    let mut out = String::new();
    let mut rest = s;
    while let Some(amp) = rest.find('&') {
        out.push_str(&rest[..amp]);
        let tail = &rest[amp..];
        let decoded = tail.find(';').and_then(|semi| {
            let name = &tail[1..semi];
            let ch = match name {
                "amp" => Some('&'),
                "lt" => Some('<'),
                "gt" => Some('>'),
                "quot" => Some('"'),
                "apos" => Some('\''),
                "nbsp" => Some(' '),
                _ => name
                    .strip_prefix("#x")
                    .or_else(|| name.strip_prefix("#X"))
                    .and_then(|h| u32::from_str_radix(h, 16).ok())
                    .or_else(|| name.strip_prefix('#').and_then(|d| d.parse().ok()))
                    .and_then(char::from_u32),
            };
            ch.map(|c| (c, semi))
        });
        match decoded {
            Some((c, semi)) => {
                out.push(c);
                rest = &tail[semi + 1..];
            }
            None => {
                out.push('&');
                rest = &tail[1..];
            }
        }
    }
    out.push_str(rest);
    out
}

#[cfg(test)]
mod tests {
    use super::*;

    fn page<'a>(pages: &'a [Page], id: &str) -> &'a Page {
        pages.iter().find(|p| p.id == id).unwrap()
    }

    #[test]
    fn reads_uncompressed_pages_by_diagram_id() {
        let xml = r##"<mxfile><diagram id="p1" name="第一頁"><mxGraphModel><root>
            <mxCell id="0"/><mxCell id="1" parent="0"/>
            <mxCell id="a" value="甲" style="rounded=1;strokeColor=#b85450;" vertex="1" parent="1"/>
            <mxCell id="b" value="乙" style="strokeColor=#000000;" vertex="1" parent="a"/>
            <mxCell id="e" style="strokeColor=#b85450;" edge="1" parent="1" source="a" target="b"/>
            </root></mxGraphModel></diagram>
            <diagram id="p2" name="第二頁"><mxGraphModel><root><mxCell id="0"/></root></mxGraphModel></diagram>
            </mxfile>"##;
        let pages = parse(xml).unwrap();
        assert_eq!(
            pages.iter().map(|p| p.id.as_str()).collect::<Vec<_>>(),
            ["p1", "p2"]
        );
        let p1 = page(&pages, "p1");
        let red: Vec<&str> = p1
            .cells
            .iter()
            .filter(|c| c.is_red_frame())
            .map(|c| c.id.as_str())
            .collect();
        assert_eq!(red, ["a"], "線不算紅框");
        let b = p1.cells_with_id("b").next().unwrap();
        assert_eq!(b.parent.as_deref(), Some("a"));
        assert_eq!(b.label(), "乙");
    }

    #[test]
    fn compressed_page_is_an_error() {
        let xml =
            r#"<mxfile><diagram id="z" name="壓縮">7VxbV+I6FP41PMLqPe1jW3B0</diagram></mxfile>"#;
        let err = parse(xml).unwrap_err();
        assert!(err.contains("請存成未壓縮"), "{err}");
        assert!(err.contains('z'), "{err}");
    }

    #[test]
    fn reads_object_and_user_object_wrappers() {
        let xml = r##"<mxfile><diagram id="p"><mxGraphModel><root>
            <mxCell id="0"/><mxCell id="1" parent="0"/>
            <object id="o1" label="包裝甲" note="x"><mxCell style="strokeColor=#B85450;" vertex="1" parent="1"/></object>
            <UserObject id="u1" label="包裝乙"><mxCell style="fillColor=#ffffff;" vertex="1" parent="o1"/></UserObject>
            </root></mxGraphModel></diagram></mxfile>"##;
        let pages = parse(xml).unwrap();
        let p = page(&pages, "p");
        let o1 = p.cells_with_id("o1").next().unwrap();
        assert!(o1.is_red_frame());
        assert_eq!(o1.label(), "包裝甲");
        let u1 = p.cells_with_id("u1").next().unwrap();
        assert!(!u1.is_red_frame());
        assert_eq!(u1.parent.as_deref(), Some("o1"));
        assert_eq!(u1.label(), "包裝乙");
    }

    #[test]
    fn html_value_is_stripped_and_unescaped() {
        let xml = r##"<mxfile><diagram id="p"><mxGraphModel><root>
            <mxCell id="h" value="外部入口&lt;br&gt;首次導入&amp;nbsp;&lt;b&gt;A&amp;amp;B&lt;/b&gt; &amp;#x4E00;" vertex="1" parent="1"/>
            </root></mxGraphModel></diagram></mxfile>"##;
        let pages = parse(xml).unwrap();
        let h = page(&pages, "p").cells_with_id("h").next().unwrap();
        assert_eq!(h.label(), "外部入口 首次導入 A&B 一");
    }

    #[test]
    fn diagram_without_id_is_an_error() {
        let xml = r#"<mxfile><diagram name="無 id"><mxGraphModel><root/></mxGraphModel></diagram></mxfile>"#;
        assert!(parse(xml).unwrap_err().contains("<diagram id>"));
    }
}
