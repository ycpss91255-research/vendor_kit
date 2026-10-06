//! 根 `justfile` 裡已占用的名字（04 命名空間：`<ns>` 不得與根 `justfile` 的 recipe 或 module 撞名）。
//! 照抄 engine/add 的 `justfile` 模組：指令之間互不依賴。
//!
//! 引擎 image 裡沒有 just，所以這裡只做保守的逐行掃描，只看頂層（不縮排）的行：
//!
//! - `mod <名>`、`mod? <名>`（後面可接路徑）：module。
//! - `<名> …:`、`@<名> …:`（冒號後不是 `=`）：recipe。
//! - 空行、註解、屬性（`[…]`）、縮排的行（recipe 本體與續行）、`name := …` 指派，以及
//!   `set`、`export`、`unexport`、`alias`、`import`、`import?` 開頭的行都跳過。
//! - 三引號字串與三反引號（`'''`、`"""`、```` ``` ````）之間的行跳過。
//!
//! 已知的限制（PR 列為缺口）：不跟進 `import` 的檔、不認 `alias` 的名字、只讀名為 `justfile` 的檔
//! （`Justfile`、`.justfile` 不讀）、不處理以 `\` 接續的頂層行。

/// 根 `justfile` 頂層的 recipe 與 module 名，依出現順序。
#[derive(Debug, Clone, Default, PartialEq, Eq)]
pub struct Names {
    pub recipes: Vec<String>,
    pub modules: Vec<String>,
}

/// just 名稱的開頭長度：`[A-Za-z_][A-Za-z0-9_-]*`；不是名稱回 0。
fn name_len(s: &str) -> usize {
    let b = s.as_bytes();
    match b.first() {
        Some(c) if c.is_ascii_alphabetic() || *c == b'_' => {}
        _ => return 0,
    }
    b.iter()
        .take_while(|c| c.is_ascii_alphanumeric() || **c == b'_' || **c == b'-')
        .count()
}

const KEYWORDS: [&str; 6] = ["set", "export", "unexport", "alias", "import", "import?"];
const FENCES: [&str; 3] = ["'''", "\"\"\"", "```"];

/// 掃描根 `justfile` 的內容。
pub fn scan(text: &str) -> Names {
    let mut names = Names::default();
    let mut fence: Option<&str> = None;
    for raw in text.lines() {
        let line = raw.strip_suffix('\r').unwrap_or(raw);
        if let Some(f) = fence {
            if line.matches(f).count() % 2 == 1 {
                fence = None;
            }
            continue;
        }
        if let Some(f) = FENCES.iter().find(|f| line.matches(**f).count() % 2 == 1) {
            fence = Some(f);
            // 開頭那一行本身仍可能是指派，照樣往下判斷（指派不記名字）。
        }
        let Some(first) = line.chars().next() else {
            continue;
        };
        if first.is_whitespace() || first == '#' || first == '[' {
            continue;
        }
        let word = line.split_whitespace().next().unwrap_or("");
        if word == "mod" || word == "mod?" {
            let rest = line[word.len()..].trim_start();
            let n = name_len(rest);
            if n > 0 {
                names.modules.push(rest[..n].to_owned());
            }
            continue;
        }
        if KEYWORDS.contains(&word) {
            continue;
        }
        let body = line.strip_prefix('@').unwrap_or(line);
        let n = name_len(body);
        if n == 0 {
            continue;
        }
        let rest = body[n..].trim_start();
        if rest.starts_with(":=") {
            continue;
        }
        let is_recipe = match rest.find(':') {
            Some(i) => rest.as_bytes().get(i + 1) != Some(&b'='),
            None => false,
        };
        if is_recipe {
            names.recipes.push(body[..n].to_owned());
        }
    }
    names
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::expect_used)]
mod tests {
    use super::*;

    #[test]
    fn top_level_recipes_and_modules() {
        let text = "\
# comment
set shell := [\"bash\", \"-c\"]
version := '1.0'
export FOO := \"x\"
alias b := build
import '.vendor_kit/entry.just'
mod tools
mod? extra 'extra/mod.just'

[private]
build target='x:y' *args: deps
    echo {{target}}
@quiet:
    echo hi
default: build
notes := '''
fake:
'''
";
        let names = scan(text);
        assert_eq!(names.recipes, ["build", "quiet", "default"]);
        assert_eq!(names.modules, ["tools", "extra"]);
    }

    #[test]
    fn crlf_and_empty_input() {
        assert_eq!(scan(""), Names::default());
        let names = scan("a:\r\n\techo\r\nmod m\r\n");
        assert_eq!(names.recipes, ["a"]);
        assert_eq!(names.modules, ["m"]);
    }
}
