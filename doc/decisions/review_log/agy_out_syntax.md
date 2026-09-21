本整理基於 **POSIX.1-2017 / The Open Group Base Specifications**、**Linux man-pages(7)**、**GNU Coding Standards**、**docopt 規範**以及主流 CLI 工具官方文件。

---

### 一、POSIX / Open Group「Utility Argument Syntax」（Chapter 12）

POSIX 標準在 IEEE Std 1003.1 / The Open Group Base Definitions 第 12 章（[12.1 Utility Argument Syntax](https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap12.html) 與 [12.2 Utility Syntax Guidelines](https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap12.html#tag_12_02)）中正式規範了指令列參數的語法表示法（SYNOPSIS）：

1. **必填（Mandatory / Required）**：
   - 項目**不加中括號 `[ ]`** 即代表必填。
   - POSIX 12.1 第 8 點明訂：「當選項未被 `[` 與 `]` 包夾時，代表在該 SYNOPSIS 版本中該選項為必填（When an option is shown without the '[' and ']' brackets, it means that option is required for that version of the SYNOPSIS）。」
2. **可省略（Optional）**：
   - 使用**中括號 `[ ]`**（brackets）包夾。
   - POSIX 12.1 第 7 點：「被 `[` 與 `]` 包夾的參數或選項參數為可選（optional），可以被省略。符合標準的應用程式在實際輸入時不得包含 `[` 與 `]` 符號。」
3. **互斥二選一（Mutually Exclusive）**：
   - 使用**垂直線 `|`（vertical-line）** 分隔。
   - POSIX 12.1 第 8 點：「以 `|` 分隔的參數表示彼此互斥（mutually-exclusive）。此外，互斥的選項與運算元也可以透過列出**多行 SYNOPSIS** 來表示。」
   - 範例：`[-d|-e]` 或拆成多行展示彼此不相容的語法分支。
4. **可重複（Repeatable）**：
   - 使用**省略號 `...`（ellipses）**。
   - POSIX 12.1 第 9 點：「`...` 表示其前方的運算元允許出現一次或多次。若選項或運算元後面跟著 `...` 且整體被中括號 `[ ]` 包夾（如 `[-g arg]...` 或 `[operand...]`），則表示可以出現零次或多次；若未加括號（如 `utility -f arg [-f arg]...`），則代表至少必須出現一次。」
5. **佔位符（Placeholders / Parameters）**：
   - POSIX 12.1 第 4 點明訂：需要被實際數值替換的參數名稱，通常使用**內嵌底線**表示（例如 `option_argument`、`parameter_name`），在排版上通常使用*斜體（italics）*；另一種替代方式是使用**尖括號 `<>`**（例如 `<parameter name>`）。標準特別強調：尖括號僅是用於表示單一參數詞組的符號分組（symbolic grouping），實際輸入時不得打出 `<>`。

*來源：[The Open Group Base Specifications Issue 7 - Chapter 12 Utility Conventions](https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap12.html)*

---

### 二、GNU / man page（man-pages(7)、docopt、help2man）的慣例

在 Linux 與 GNU 開發生態中，SYNOPSIS 的慣例延續了 POSIX，並在終端機純文字展示、巨集格式化及解析器自動化上進行了細化：

1. **佔位符的呈現：`<x>` vs 斜體 vs 全大寫**：
   - **man-pages(7)**（roff/groff 格式）：依據 [man-pages(7) SYNOPSIS 段落規範](https://man7.org/linux/man-pages/man7/man-pages.7.html)，原樣輸入的指令與選項使用**粗體（boldface）**，可替換的參數/佔位符一律使用**斜體（italics）**（在 groff 原始碼中使用 `.I`、`.BI` 巨集；在終端機中可能渲染為底線或斜體）。
   - **GNU `--help` / help2man**：依據 [GNU Coding Standards](https://www.gnu.org/prep/standards/standards.html) 與 [help2man 規範](https://www.gnu.org/software/help2man/)，在不具備富文本格式的終端機純文字輸出中，佔位符通常使用**全大寫字母（UPPERCASE）**表示，例如：
     `Usage: grep [OPTION]... PATTERNS [FILE]...`
     `help2man [OPTION]... executable`
   - **docopt 規範**：依據 [docopt.org 規格說明](http://docopt.org/)，位置參數（positional argument）允許兩種等價形式：以尖括號包夾的單詞（如 `<file>`、`<host>`）或是全大寫單詞（如 `FILE`、`HOST`）。
2. **`[x]`（可省略）**：
   - 在 man-pages(7) 與 docopt 中，中括號 `[ ]` 均表示 optional，與 POSIX 定義完全一致。
3. **必選其一：`{a|b}` vs `(a|b)`**：
   - **`docopt` 標準規範**：明確規定使用**圓括號 `( )`** 來表示必填群組（required elements）。當互斥元素必須二選一時，寫為 `(a | b)` 或 `(a|b)`。docopt 說明：「當互斥情況必須擇一時，使用圓括號 `( )` 進行分組（Use parens ( ) to group elements when one of the mutually exclusive cases is required）。」
   - **man page / EBNF 大括號流派 `{a|b}`**：在擴展巴科斯範式（EBNF）及許多 Unix/Linux man pages、RFC 和 Cisco/PowerShell 規範中，使用**大括號 `{ }`** 代表必選群組（mandatory group），因此 `{a|b}` 常用來代表「必須在 a 與 b 之中擇一」，與表示可選二選一的 `[a|b]` 形成直觀對比。
   - **POSIX 傳統做法**：POSIX 標準本身不傾向在行內增加 `{}` 或 `()`，而是傾向直接將互斥分支拆寫為多行 SYNOPSIS。
4. **可省略的其一：`[a|b]`**：
   - 由中括號與垂直線組合，表示「可從中選一個，或者都不選（zero or one）」。
5. **選項與參數等價語法（GNU getopt / getopt_long 規則）**：
   - **旗標（boolean flag，無參數）**：`--flag` 或 `-f`。
   - **短選項帶參數**：`-x VALUE` 與 `-xVALUE` 等價。
   - **長選項帶參數**：`--long=VALUE` 與 `--long VALUE` 等價。
     - *重要特例*：若參數為「可選參數（optional argument）」，依據 GNU `getopt_long(3)` 規則，長選項必須使用等號（`--long=VALUE`），短選項必須緊接（`-xVALUE`），不可留空格，否則解析器無法判斷下一個 token 是該選項的參數還是獨立的位置參數。
   - **說明清單中的簡寫**：在 `--help` 輸出中常以逗號並列，如 `-x, --long=VALUE`，表示兩者為長短選項對應關係。

*來源：[Linux man-pages: man-pages(7)](https://man7.org/linux/man-pages/man7/man-pages.7.html) | [docopt 語言標準](http://docopt.org/) | [GNU Coding Standards](https://www.gnu.org/prep/standards/standards.html)*

---

### 三、主流工具 Usage 行實例剖析

#### 1. Git（以 `git-branch` 為例）
來源：[git-scm.com/docs/git-branch](https://git-scm.com/docs/git-branch)

**原文節錄**：
```text
git branch ( -m | -M ) [<old-branch>] <new-branch>
git branch ( -d | -D ) [ -r ] <branch-name>…​
git branch [ --track [ = ( direct | inherit )] | --no-track ] [ -f ] [ --recurse-submodules ] <branch-name> [<start-point>]
```

**解析**：
- **必選其一互斥**：採用圓括號配垂直線 `( -m | -M )` 與 `( -d | -D )`，代表重命名或刪除時必須明確指定其中一種強度旗標。
- **可選互斥**：`[ --track [ = ( direct | inherit )] | --no-track ]`，最外層以 `[ ... | ... ]` 表示追蹤模式互斥且可選。
- **可選內嵌參數與預設值選項**：`[ = ( direct | inherit )]` 展示了可選的 `=` 符號，等號後以 `( direct | inherit )` 規範了枚舉值的必選二選一。

#### 2. Docker（以 `docker image tag` 與 `docker run` 為例）
來源：[Docker Documentation: docker image tag](https://docs.docker.com/reference/cli/docker/image/tag/)、[Docker Documentation: docker run](https://docs.docker.com/reference/cli/docker/container/run/)

**原文節錄**：
```text
Usage:  docker image tag SOURCE_IMAGE[:TAG] TARGET_IMAGE[:TAG]
Usage:  docker run [OPTIONS] IMAGE [COMMAND] [ARG...]
```

**解析**：
- **佔位符風格**：使用 GNU 風格的純大寫英文單詞（`SOURCE_IMAGE`、`TARGET_IMAGE`、`IMAGE`）。
- **可選版本/標籤後綴**：`SOURCE_IMAGE[:TAG]`。在佔位符後直接緊貼 `[:TAG]`，外圍中括號代表該部分可省略，但若要指定 tag，前綴冒號 `:` 為語法的一部分。

#### 3. npm（以 `npm install` 為例）
來源：[npm Docs: npm-install](https://docs.npmjs.com/cli/commands/npm-install)

**原文節錄**：
```text
npm install [<@scope>/]<name>
npm install [<@scope>/]<name>@<tag>
npm install [<@scope>/]<name>@<version>
```
*(在綜合手冊與通用 CLI 文件中通常合寫為：`npm install [<@scope>/]<name>[@<version>]`)*

**解析**：
- **佔位符風格**：採用 `<name>`、`<version>`、`<tag>` 角括號佔位符。
- **可選前綴與可選版本後綴**：
  - `[<@scope>/]`：可選的組織作用域前綴，包含結尾的 `/`。
  - `[@<version>]`：可選的版本後綴，中括號內包含版本識別前綴 `@`，表示若省略版本則安裝最新預設版本。

---

### 四、結論

#### 1. POSIX / GNU / docopt 通用記法對照表

| 記法 (Notation) | 語法意義 (Meaning) | 典型範例 | 規範來源 |
| :--- | :--- | :--- | :--- |
| **`literal`** (粗體 / 直接書寫) | 原樣輸入的指令、子命令或旗標名稱 | `git`、`install`、`-v` | [POSIX 12.1](https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap12.html)、[man-pages(7)](https://man7.org/linux/man-pages/man7/man-pages.7.html) |
| **`[ ... ]`** | **可選（Optional）**：內容可省略，可出現 0 或 1 次 | `[-f]`、`[<file>]` | [POSIX 12.1](https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap12.html) |
| **`...`** (Ellipsis) | **可重複（Repeatable）**：前一項可出現 1 次或多次 | `FILE...`、`[ARG...]` | [POSIX 12.1](https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap12.html) |
| **`[ ... ]...`** | **可重複可選**：可出現 0 次或多次 | `[OPTION]...`、`[FILE...]` | [POSIX 12.1](https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap12.html) |
| **`\|`** (Pipe) | **互斥（Mutually Exclusive）**：二選一或多選一 | `a \| b` | [POSIX 12.1](https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap12.html) |
| **`[ a \| b ]`** | **可選互斥**：從 a 與 b 中最多選一個，亦可都不選 | `[-a \| -b]` | [docopt](http://docopt.org/)、[POSIX 12.1](https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap12.html) |
| **`( a \| b )`** 或 **`{ a \| b }`** | **必選互斥**：必須嚴格二選一 | `(-m \| -M)`、`{start\|stop}` | [docopt](http://docopt.org/)、[Git docs](https://git-scm.com/docs/git-branch) |
| **`*name*`** / **`<name>`** / **`NAME`** | **參數佔位符**：由使用者替換為實際值 | `<branch-name>`、`FILE` | [POSIX 12.1](https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap12.html)、[GNU Standards](https://www.gnu.org/prep/standards/standards.html) |
| **`name[delimiter<suffix>]`** | **可選後綴**：相鄰黏合的可選標籤/版本 | `IMAGE[:TAG]`、`<pkg>[@<ver>]` | 主流套件管理與容器慣例 |

---

#### 2. 特別解答：「二選一」在 Linux 慣例中的符號與流派

1. **二選一符號一律為 `|`（垂直線），絕對不是 `a／b`**：
   - **語法規範標準**：無論是 POSIX.1-2017（12.1 第 8 條）、Linux man-pages(7)、GNU Coding Standards、還是 docopt，**表示互斥選擇的標準符號只有垂直線 `|`（vertical bar）**。
   - **為什麼不能用斜線 `/`**：
     - **路徑衝突**：在 Unix/Linux 架構中，正斜線 `/` 是根目錄與路徑分隔符（Path separator）。若在參數語法中使用 `a/b`，會與檔案路徑（如 `path/to/file`）或帶作用域的名稱（如 `@scope/pkg`）產生嚴重的語法歧義。
     - **形式文法傳承**：`|` 自 1960 年代 BNF（巴科斯範式）開始就是形式文法中表示「選擇/Alternation」的公認符號，正則表達式（Regex）亦同。
     - **少數非標準特例**：日常非正式討論、簡易 README、或是早期 MS-DOS / Windows 命令行手冊（因 DOS 早期使用 `/` 作為選項前綴，如 `/s /q`）偶爾會見到 `y/n` 或 `-y/--yes`，但在任何 Linux / POSIX 官方規範中均屬非正式寫法。

2. **「必選二選一」的括號流派差異**：
   - **`docopt` 與 Git 流派——圓括號 `(a|b)`**：
     `docopt` 正式定義中，中括號代表 optional，圓括號代表 required grouping。因此 `(a|b)` 是現代 CLI 解析器與 Git 等工具官方手冊中標註「必選二選一」最常見的寫法。
   - **EBNF 與系統服務手冊流派——大括號 `{a|b}`**：
     源自標準 EBNF 文法與部分 Unix/Linux init 腳本（例如 `/etc/init.d/service {start|stop|restart}`）以及網通設備（Cisco/Juniper）手冊。在這些文件中，大括號代表必選集合（required set），與代表可選的中括號 `[a|b]` 形成對稱。
   - **POSIX 原生流派——拆分多行 SYNOPSIS**：
     POSIX 官方標準在遇到頂層必填互斥時，傾向不依賴額外括號，而是直接列出多行獨立的 SYNOPSIS（如 `utility_name -d ...` 與 `utility_name -e ...`），以最嚴謹的方式消除括號巢狀帶來的歧義。
