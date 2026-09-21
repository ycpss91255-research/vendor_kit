# ---------- 審閱頁（md 定稿版逐字移植）共用 ----------
def M(s):
    """md 行內記法 → 圖上文字：`code` 去反引號；**x** → 粗體。其餘一字不改。"""
    s = s.replace("`", "")
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
def sec(out, pid, y, title, w=1560):
    """節標題（LBL）。回傳結束 y。"""
    out.append(v(pid, "1", LBL, title, 40, y, w, 28)); return y + 32
def para(out, pid, y, text, style=None, w=1560, x=40, pad=6):
    """一段文字一格（白底 12pt）。回傳結束 y（含 10px 間距）。"""
    st = style or LT12
    h = hv(text, w, pad=pad)
    out.append(vb(pid, "1", st, text, x, y, w, h)); return y + h + 10
def mtbl(out, prefix, y, cols, rows, x=40, bold0=True):
    """md 表格 → tbl()（表頭灰底、第一欄粗體）；rows 內每格先過 M()。回傳結束 y（含 14px 間距）。"""
    return tbl(out, prefix, "1", x, y, cols, [[M(c) for c in r] for r in rows], bold0=bold0) + 14
def rtitle(pid, title):
    return [v("title", "1", TITLE, title, 40, 20, 1400, 34)]

# ================= P0 v1p0：審閱頁 00 名詞與縮寫（1）=================
p0 = rtitle("p0", "審閱頁 00：名詞與縮寫（1）三方／組件／常用詞")
Y = 70
Y = para(p0, "p0_intro", Y, M("本頁是所有審閱頁的共同字典：之後每一頁只用這裡定義的詞。本頁只定義、不決議。審閱方式：逐條看名稱與定義是否貼切，不貼切的寫一句理由。"))
# ---- 三方與承諾關係 ----
Y = sec(p0, "p0_s1", Y, "三方與承諾關係")
Y = mtbl(p0, "p0_t1", Y, [("名稱", 150), ("是誰", 300), ("跟 VK 的互動", 850), ("地位", 260)], [
 ["**下游開發者**", "開發下游 repo 的人", "照 `dist/` 出貨契約把工具打成下游 image；用 dev／undev 在本機開發工具", "被承諾方"],
 ["**下游使用者**", "在專案裡接入、升級、使用工具的人，含只打 `just <ns> …` 的人", "跑 `bootstrap.sh` 接入；回答詢問或給 `-y`；commit 薄殼與版本鎖定行；升版後若有衝突，手動編輯再重跑", "被承諾方"],
 ["**VK**", "我們，vendor_kit 開發者", "維護引擎 image 與薄殼（含啟動器），履行對兩方的承諾；內部實作不屬契約、可變更", "承諾方"],
])
Y = para(p0, "p0_t1n", Y, M("同一人可兼兩種身分（例如自己寫工具、自己在專案裡用）。圖文一律寫全名，不縮寫。"))
Y = para(p0, "p0_t2l", Y, M("兩種 repo 要分清楚："))
Y = mtbl(p0, "p0_t2", Y, [("中文名", 150), ("英文", 200), ("定義", 1210)], [
 ["**專案**", "project", "下游使用者的 git repo（或 monorepo 裡的一個子專案）：接入 VK 後含 `.vendor_kit/`；VK 的動詞都在專案裡跑"],
 ["**下游 repo**", "downstream repo", "提供工具的 git repo；把 `dist/` 用三行 Dockerfile 打成純資料的下游 image 推到 registry（公開或私有，由下游開發者自決；私有需憑證）。`<repo>` 是它的名字"],
])
# ---- VK 組件 ----
Y = sec(p0, "p0_s2", Y, "VK 組件（component）")
Y = para(p0, "p0_c0", Y, M("VK 由三個組件組成；組件是對外可見的最大單位，模組是組件內部的程式單元，**組件 > 模組**。"))
COMP = [
 M("**引擎**：VK 的主程式，是容器 image；所有判斷與寫檔都在裡面做，只透過掛入的 `/repo` 看專案根。"),
 M("**薄殼**：`.vendor_kit/` 內進 git、由引擎產生、人不改的五個檔（`entry.just`、`vendor.just`、`log.sh`、`.gitignore`、`ci/check.sh`）；五檔用同一套自描述標頭（通常在首行，`ci/check.sh` 在第二行）與 hash 契約。"),
 M("**啟動器**：薄殼內的 POSIX sh 片段，負責拉 image、展開工具內容、起引擎容器；`bootstrap.sh` 是第一次接入時的啟動器。"),
]
CW = 510; ch = max(hv(t, CW) for t in COMP)
for i, t in enumerate(COMP):
    p0.append(vb(f"p0_c{i + 1}", "1", LT12, t, 40 + i * (CW + 15), Y, CW, ch))
Y += ch + 10
Y = sec(p0, "p0_s2b", Y, "VK 模組（module）——引擎內的 8 個程式單元")
Y = mtbl(p0, "p0_t3", Y, [("中文名", 150), ("英文代號", 150), ("做什麼", 1260)], [
 ["版本解析", "`resolve`", "讀版本鎖定行、查 registry 最新版、算出這次要拉哪些 image、寫哪些檔"],
 ["取件", "`fetch`", "把展開的工具內容寫進 `cache/`、逐檔驗指紋、寫印記"],
 ["初始檔合併", "`initfile`", "依工具宣告建初始檔、存基準版、升版時做三方合併"],
 ["薄殼產生", "`shell`", "產生或重產薄殼五檔與自描述標頭，並比對薄殼是否被改"],
 ["進度與寫入", "`progress`", "建、恢復、刪進度檔；鎖；原子替換，讓可寫動詞中斷後能接續"],
 ["設定與格式", "`schema`", "讀寫 VK 檔的 TOML：檔案版檢查、未知欄位保留、`config.toml`"],
 ["紀錄", "`log`", "每次執行寫一份執行紀錄"],
 ["清理", "`prune`", "找出版本鎖定行與本機覆寫都未引用的舊 image、殘留容器與暫存並刪除"],
], bold0=False)
# ---- 常用詞 ----
Y = sec(p0, "p0_s3", Y, "常用詞")
Y = mtbl(p0, "p0_t4", Y, [("中文名", 190), ("英文", 170), ("定義", 1200)], [
 ["**專案檔**", "project file", "根 `justfile`、根 `.dockerignore`、建立後歸下游使用者的初始檔，以及專案裡其他原有的檔。VK 對它們只守專案檔四原則"],
 ["**VK 檔**", "VK file", "VK 自己建、自己管的檔，全在 `.vendor_kit/` 內：`version.toml`、`version.local.toml`、`config.toml`、薄殼、基準版與 metadata、`cache/`、`gen/`、進度檔、執行紀錄"],
 ["**進 git 的檔**", "tracked file", "會被 commit 的檔；在 VK 檔中是 `version.toml`、`config.toml`、薄殼、基準版與 metadata；專案檔一律視為進 git 的檔"],
 ["**版本鎖定行**", "lock line", "`.vendor_kit/version.toml` 內每個工具（與引擎）各一行；進 git；只有這行決定裝哪一版。**唯一正規形**：引擎行在檔案頂層 `vendor_kit = \"<image>:<tag>@sha256:<digest>\"`；工具行在 `[tools]` 表下 `<repo> = \"<image>:<tag>@sha256:<digest>\"`（`<repo>` 是未加引號的 TOML 鍵，名稱規則見佔位符）。每行：行首無空白、鍵後一個空白、`=`、一個空白、雙引號字串、無尾端註解、LF 結尾；引擎寫出一律此形。禁 BOM、禁重複鍵、禁 TOML 表旁路寫法（例如 `[tools.<repo>]`、`[vendor_kit]`）；引擎讀到非正規形 → 1 列出差異、不動。頂層另有 `schema`、`written_by` 兩個欄位，與 `[tools]` 下的工具行不同層、不會撞名"],
 ["**正式版**", "release version", "registry 上的正式 tag（排除預發行如 `-rc`、`-beta`）；沒指定 `@<tag>` 時「最新版」一律指最新正式版"],
 ["**初始檔**", "init file", "工具在 `dist/init.toml` 宣告、`add` 時建進專案的檔，分兩型：**copy 型**（`strategy = copy`，預設；整檔複製成專案裡的新檔）、**append 型**（`strategy = append`；把幾行插進專案既有檔，不整檔複製）；建立後歸下游使用者、進 git"],
 ["**基準版**", "baseline", "`.vendor_kit/baseline/<repo>/` 內上次套用的初始檔原版副本；進 git；升版時三方合併的共同祖先（另兩份是下游使用者的現況與新版初始檔）"],
 ["**三方合併**", "three-way merge", "升版時對每個納管初始檔拿基準版（共同祖先）、下游使用者現況、新版三份做的合併；兩邊都改的地方合不起來就在檔內留衝突標記"],
 ["**metadata**", "metadata", "基準版旁的 `.vendor_kit.toml`：記每個初始檔的來源、狀態（納管／拒絕過…）、進行中的進度；進 git"],
 ["**可寫動詞**", "writing verb", "會建進度檔的動詞：install、uninstall、add、remove、upgrade（含升引擎）、dev、undev、prune"],
 ["**唯讀動詞**", "read-only verb", "不建進度檔的動詞：update、sync、help；都不寫進 git 的檔、也不恢復進度檔。`sync` 仍會寫 `cache/`、`gen/`（不進 git）"],
 ["**進度檔**", "progress file", "可寫動詞的交易紀錄；成功即刪；中斷後下次可寫動詞先恢復再繼續（prune 例外：遇活躍進度檔只列出提示、不恢復、不阻擋）。兩種落點：`.vendor_kit/.tmp.<verb>.<id>.toml`（install、uninstall、remove、undev、prune、dev、升引擎用）與 metadata 內的 `[progress]`（add、`upgrade <repo>` 用）"],
 ["**執行紀錄**", "run log", "`.vendor_kit/log/<verb>/<時間戳>-<id>.jsonl`；每個動詞及每次 `bootstrap.sh` 執行各一檔（`bootstrap.sh` 自己那段寫在 `log/bootstrap/`）；不進 git；事後追溯用。順序：不寫檔、不拉 image、不起容器的前置檢查（是否 git repo、just 版本）可在建紀錄之前；任何寫入、拉取、起引擎之前必已有紀錄；紀錄建不了就不做任何事"],
 ["**CI 模式**", "CI mode", "環境變數 `CI` 為真（非空且不是 `0`／`false`）時的模式：不寫任何進 git 的檔、不查最新版（`update` 除外：它的用途就是查）"],
 ["**需人處理**", "needs human", "動詞停下並印出下一步指令的結束：結束碼 1 或 3 且附指令，衝突 2 亦同；圖上橙色"],
 ["**失敗**", "failure", "拉不到、寫不進、驗證不過這類無法繼續的結束；印原因；結束碼 1；圖上紅色"],
 ["**專案檔四原則**", "four rules", "① 可以建，但要明說建了什麼；② 要改先問，`-y` 免問；③ 永不刪；④ 永不覆蓋（不用工具版本取代客製內容）"],
 ["**預檢**", "precheck", "動詞在寫任何檔之前做的全部檢查（撞名、憑證、dev 中、要問什麼）；多工具動詞先對全部工具預檢完，任一不過就整體不動"],
 ["**resolve／apply（兩段式）**", "two-phase", "兩段式動詞（add、remove、upgrade、sync、undev、uninstall、prune）分兩段、最多起兩個引擎容器：先在唯讀的 resolve 容器算計畫與指紋，啟動器再拉 image（需要新版內容的動詞才拉），最後在 apply 容器重驗指紋後寫入（`sync` 算出沒事做時到 resolve 為止）；單段動詞（install、升引擎、update、dev、help）只有一個容器"],
 ["**介面版**", "protocol version", "薄殼與引擎之間的整數版號 `P`；薄殼每次呼叫附上；與 release 版號無關"],
 ["**檔案版**", "schema version", "VK 寫的每個 TOML 內的 `schema = N`；決定引擎能不能讀這個檔"],
 ["**最低介面版**", "floor", "引擎仍支援的最低介面版；固定常數；只能經 ADR 提高"],
 ["**結束碼**", "exit code", "`0` 成功（含 warn）；`1` 需人處理或失敗（哪一種由訊息語意決定，不由碼決定）；`2` 合併衝突（留標記、基準版仍推到新版；合併結果是 TOML／just 而解析不過的檔 → 也是 2，但留原檔、該檔基準版不推）；`3` 介面版／檔案版不合，先升級或退回，零寫入"],
 ["**本機覆寫**", "local override", "`version.local.toml` 內由 dev（或 `bootstrap.sh --local`）寫的項目，每個工具或引擎各一項：工具那項 = 一行 `path:<dir>`，把工具指到本機目錄；引擎那項 = tag ＋ image ID 兩欄，把引擎指到本機 image（image ID 供後續驗證：啟動器每次起引擎前比對本機 image 的 ID）；不進 git；有就優先於版本鎖定行"],
 ["**symlink**", "symlink", "符號連結：一個指向別處目錄或檔案的捷徑；dev 用它讓 `cache/<repo>/` 指向本機目錄"],
 ["**hash**", "hash", "檔案內容的 sha256 指紋；同內容必同 hash。用在薄殼自描述標頭、印記、指紋重驗"],
 ["**image ID**", "image ID", "docker 本機 image 的內容 ID（`sha256:<hex64>`）；只在本機有意義，與 registry 的 digest 不同"],
 ["**tty**", "tty", "互動終端；有 tty 才能問問題。沒 tty（CI、管線）又沒 `-y` 時，需詢問的動詞以 1 結束"],
 ["**佔位符**", "placeholder", "`<repo>` 下游 repo 名，規則 `[a-z0-9_][a-z0-9_-]*`（小寫、不含句點，才能當 `[tools]` 下未加引號的 TOML 鍵；OCI repo 名本就小寫），`vendor_kit` 保留給引擎、不得作工具名；`<ns>` 工具的 just 命名空間；`<image>` image 名（含 registry 與路徑）；`<tag>` image 版本名；`<digest>` image 內容指紋的 64 位十六進位 `<hex64>`，寫法 `sha256:<digest>`；`<dir>` 目錄；`<id>` 一次執行的交易 id"],
])
c, Y = lgd("p0", 40, Y + 6, ["tblh"], "本頁只定義、不決議；續「名詞與縮寫（2）既有詞／記法／動詞」頁")
p0 += c
pages_v1_a.append(("v1p0", "名詞與縮寫（1）三方／組件／常用詞", p0))

# ================= P0b v1p0b：審閱頁 00 名詞與縮寫（2）=================
p0b = rtitle("p0b", "審閱頁 00：名詞與縮寫（2）既有詞／記法／動詞")
Y = 70
Y = sec(p0b, "p0b_s1", Y, "其他既有詞")
Y = mtbl(p0b, "p0b_t1", Y, [("中文名", 190), ("英文", 190), ("定義", 1180)], [
 ["**下游 image**", "downstream image", "`FROM scratch` 只放檔案的 image，沒有程式、不會被執行；多架構 amd64 + arm64"],
 ["**`dist/`**", "dist", "下游 repo 的出貨目錄：`files/`（全部展開到 `cache/`）、`init.toml`、`just/<ns>.just`；其他內容不出貨"],
 ["**工具 recipe**", "tool recipe", "工具的 `dist/just/<ns>.just` 提供、下游使用者以 `just <ns> …` 執行的 just 指令；相對於 VK 自己的動詞 `just vendor_kit …`。每次執行前自動觸發一次 `sync`"],
 ["**專案根**", "project root", "專案內含 `.vendor_kit/` 的目錄；不是 git toplevel；monorepo 子專案各自一套"],
 ["**`cache/`、`gen/`**", "—", "`.vendor_kit/` 內不進 git 的兩個目錄：`cache/<repo>/` 放工具內容的本機副本，`gen/` 放引擎產生、供 just 載入的檔；其中 `gen/tools.just` 是引擎產生、把各工具的 `<ns>.just` 接進 `just` 的入口檔（每個 `<ns>.just` 一行；由薄殼 `entry.just` 載入）"],
 ["**印記**", "stamp", "`gen/<repo>.stamp`：第一行 = 裝的是哪個 digest（dev 時是 `path:<dir>`），之後每檔一行指紋；只是已裝版本的快取鍵，不是信任來源"],
 ["**納管**", "managed", "初始檔經下游使用者同意建立後，VK 在 metadata 記下它的來源與狀態；拒絕建立也記（拒絕過）"],
 ["**自描述標頭**", "self-describing header", "薄殼每檔的 `# vendor_kit-shell/<介面版> engine=<引擎版> sha256=<其餘內容的 hash>`；通常在首行，檔案有 shebang 時（`ci/check.sh`）在第二行；引擎重算比對，不符就不動（規格原文稱「自描述首行」）"],
 ["**救援路徑**", "rescue path", "不依賴 `gen/` 的單段引擎呼叫；任何 ≥ 最低介面版的薄殼永久可用。兩種情境：第一次接入由 `bootstrap.sh` 啟動 `install`；既有薄殼修復用 `install` 再跑、升引擎、sync 的不符提示、help"],
])
# ---- 語法記法 ----
Y = sec(p0b, "p0b_s2", Y, "語法記法")
Y = para(p0b, "p0b_n0", Y, M("動詞表與後頁的指令寫法一律照這張表。"))
Y = mtbl(p0b, "p0b_t2", Y, [("記法", 260), ("意思", 1300)], [
 ["`<x>`", "必填佔位符"],
 ["`[x]`", "可省略"],
 ["`[@<tag>]`", "可省略的版本後綴，緊接 repo 名（`<repo>@<tag>`）"],
 ["`-x <值>`／`--long <值>`", "短／長選項等價；只有常用的才有短的"],
 ["`-y`", "不帶值的開關"],
 ["`a／b`", "二選一"],
], bold0=False)
Y = para(p0b, "p0b_o0", Y, M("動詞表用到的選項（短形只有 `-t`、`-y`、`-p`、`-i`、`-h`）："))
OPTS = [
 "`-t <repo>[@<tag>]`／`--tool <repo>[@<tag>]`：`bootstrap.sh` 要接入的工具與版本，可重複；省略 `@<tag>` = 最新正式版。",
 "`-p <dir>`／`--path <dir>`：把工具指到本機目錄（`dev <repo>`）。",
 "`-i <tag>`／`--image <tag>`：把引擎指到本機 image（`dev vendor_kit`；只能 tag）。",
 "`-y`／`--yes`：省略詢問，視同回答「是」。",
 "`--exit-code`：`update` 有新版時以結束碼 2 回報，而不是只印出來。",
 "`--dry-run`：只預覽會問什麼、會改什麼，不寫任何進 git 的檔、不建進度檔；需要新版內容的動詞（add、upgrade）仍會拉 image 展開，uninstall、remove、prune 不拉。只有這五個動詞接受。",
 "`--source <image>`：`add` 時下游 image 名不照 `<repo>-dist` 慣例時指定。",
 "`--local <tar>`：`add` 離線：只收存在的 `.tar` 離線包。`bootstrap.sh` 的 `--local <image tag／tar>` 另可收本機 image tag，值依序判別：以 `.tar` 結尾 → 檔案路徑（必須存在，否則 1）；否則值含 `/` 且存在同名檔 → 1 要求消歧；否則 → image tag。",
 "`--verify`：`sync` 逐檔驗指紋（CI 模式下本來就逐檔驗，不必加）。",
 "`--no-justfile`：`install` 跳過根 justfile 那一步，只印手動加那一行的指示。",
 "`--help`（`-h`）：印該動詞的用法；所有動詞都接受，不列在各動詞語法裡。",
 "`--timeout <秒>`：單次拉 image 的上限秒數；會拉 image 的動詞（add、upgrade、sync、undev、`bootstrap.sh`）都接受。",
]
for i, t in enumerate(OPTS):
    h = hv(M(t), 1560, pad=2)
    p0b.append(vb(f"p0b_o{i + 1}", "1", LT12, M(t), 40, Y, 1560, h)); Y += h
Y += 10
# ---- 動詞 ----
Y = sec(p0b, "p0b_s3", Y, "動詞")
Y = para(p0b, "p0b_v0", Y, M("寫法：小寫原文，前面省略 `just vendor_kit`。"))
Y = mtbl(p0b, "p0b_t3", Y, [("動詞", 330), ("做什麼", 1230)], [
 ["`install`", "第一次接入：建 `.vendor_kit/`、薄殼、`version.toml`、`config.toml`、空 `baseline/`；根 `justfile` 無 → 建四行（import、空行、`default:`、`@just --list`），有 → 問後加 import 一行；根 `.dockerignore` 無 → 建四行，有 → 問後加四行；再跑 = 冪等修復；不做 `git init`"],
 ["`uninstall`", "移除 VK 自產的檔、根 `justfile` 那一行與根 `.dockerignore` 那四行（都經詢問、只刪仍與原文相同的行，改過的跳過並 warn）；保留：執行紀錄、初始檔（只印清單）、被下游使用者改過的 `config.toml` 與薄殼、非空目錄"],
 ["`add <repo>[@<tag>]`", "接入一個工具：展開到 `cache/`、建初始檔與基準版、最後寫版本鎖定行"],
 ["`remove <repo>`", "移除該工具的版本鎖定行、`cache/`、基準版；初始檔不刪只印清單"],
 ["`update [<repo>]`", "只查有沒有新版，只寫執行紀錄；`--exit-code` 有新版回 2"],
 ["`upgrade [<repo>[@<tag>]]`", "升到最新（或指定）版：換 `cache/`、初始檔三方合併、基準版推到新版、改版本鎖定行"],
 ["`dev <repo> -p <dir>`／`dev vendor_kit -i <tag>`", "把工具指到本機目錄：寫本機覆寫、`cache/<repo>/` 改成指向 `<dir>/dist` 的 symlink、印記記 `path:<dir>`；或把引擎指到本機 image：寫本機覆寫（tag 與 image ID）。工具須已在版本鎖定行；也建進度檔"],
 ["`undev <repo>`／`undev vendor_kit`", "撤銷 dev，回到版本鎖定行的版本"],
 ["`sync [<repo>]`", "依版本鎖定行重建 `cache/` 與 `gen/`；不改任何進 git 的檔；工具 recipe 執行前自動觸發"],
 ["`prune`", "刪版本鎖定行與本機覆寫都未引用的舊 image、殘留容器／network／volume 與暫存；遇活躍進度檔只列出提示、不恢復、不阻擋"],
 ["`help`", "印命名空間層說明；不觸網、只寫執行紀錄"],
], bold0=False)
Y = para(p0b, "p0b_v1", Y, M("**升引擎** = `upgrade vendor_kit[@<tag>]`：改引擎那一行的版本鎖定行、用新引擎重產薄殼，然後回 1 要求再跑一次剛才的指令。"))
Y = para(p0b, "p0b_v2", Y, M("記法與顏色見主圖第 0 頁「圖例與記法」；審閱規則見 AGENTS.md。"), style=TEXT(12) + "align=left;")
# ---- 寫法約定 ----
Y = sec(p0b, "p0b_s4", Y, "寫法約定")
Y = para(p0b, "p0b_w1", Y, M("「→ 1：X」= 以結束碼 1 結束並印出 X；「→ 0」= 以結束碼 0 結束。「→ 2」「→ 3」同理。"), style=RULE)
Y = para(p0b, "p0b_w2", Y, M("圖上顏色：**藍** = 引擎做；**白** = 啟動器做；**綠** = 結束碼 0；**橙** = 需人處理；**紅** = 失敗；**白虛線橢圓** = 來自其他頁的節點。"), style=RULE)
c, Y = lgd("p0b", 40, Y + 6, ["tblh", "ruleb"], "續「名詞與縮寫（1）三方／組件／常用詞」頁；本頁只定義、不決議")
p0b += c
pages_v1_a.append(("v1p0b", "名詞與縮寫（2）既有詞／記法／動詞", p0b))

# ================= P1 v1p1：審閱頁 01 不變量與角色 =================
p1 = rtitle("p1", "審閱頁 01：不變量與角色")
Y = 70
Y = para(p1, "p1_intro", Y, M("本頁是契約的第一頁：只用第 0 頁「名詞與縮寫」與本頁名詞表定義的詞，不引用後面的頁。只摘錄、不新增決議；每條的出處列在文末「出處對照」。審閱方式：逐條打勾／打叉，叉的寫一句理由。"))
Y = sec(p1, "p1_s0", Y, "一句話目的")
Y = para(p1, "p1_goal", Y, M("下游 repo 把要交付的檔案打成一個純資料的下游 image 推到 registry（公開或私有，由下游開發者自決；私有需憑證）；下游使用者在專案裡跑一支接入腳本後，用 `just vendor_kit <動詞>` 取得工具、把版本鎖成一行、初始檔以三方合併升版。VK 只負責搬移，不承諾搬來的內容可執行。"), style=RULE)
Y = sec(p1, "p1_s1", Y, "本頁名詞（第 0 頁沒有的頁內特有詞）")
Y = mtbl(p1, "p1_tm", Y, [("名詞", 170), ("定義", 1390)], [
 ["GHCR", "GitHub 的容器 registry；引擎放的地方，也是下游 image 的預設落點（下游 image 公開或私有由下游開發者自決）。"],
 ["`config.toml`", "`.vendor_kit/config.toml`，VK 的設定檔，進 git；升引擎時比照初始檔三方合併。"],
 ["衝突標記", "三方合併合不起來時留在檔內的 `<<<<<<<`／`>>>>>>>` 標記；升版逐檔的結果：沒改 → 換新版；只有下游使用者改 → 不動；兩邊都改 → 三方合併，合不起來就留衝突標記、結束碼 2。"],
 ["交付物", "工具 recipe（`just <ns> …`）產生、要交給別人用的東西（例如 deploy 包）。"],
 ["契約檢查腳本", "`.vendor_kit/ci/check.sh`，薄殼之一，兩種用法分開：不帶參數 = 下游 CI 的唯一入口（在專案裡跑同步、驗證、試跑升版、工具與專案測試）；`--dist` = 下游開發者在下游 repo 裡驗 `dist/` 佈局與兩平台一致。"],
 ["下游 CI", "專案自己的 CI 平台；不是「方」。"],
 ["Renovate", "下游使用者自選的版本更新機器人；不是「方」。"],
])
# ---- 三方角色表 ----
Y = sec(p1, "p1_s2", Y, "三方角色與承諾關係")
Y = mtbl(p1, "p1_tr", Y, [("名稱", 120), ("是誰", 200), ("負責", 580), ("不負責", 340), ("地位", 320)], [
 ["**下游開發者**", "開發下游 repo 的人", "維護 `dist/` 與三行 Dockerfile；在下游 repo 的 CI 用契約檢查腳本 `--dist` 驗 `dist/` 佈局與兩平台一致；自己在乾淨機器驗交付物可執行；把下游 image 推到 registry（公開或私有自決；私有時下游使用者要備憑證）；用 dev／undev 在本機開發工具", "不碰專案的檔；交付物不得依賴 `.vendor_kit/`；交付物的可執行性不由 VK 代驗", "被承諾方：只要照 `dist/` 契約出貨，VK 保證搬得到、鎖得住、升得了"],
 ["**下游使用者**", "在專案裡接入、升級、使用工具的人，含只打 `just <ns> …` 的人", "跑 `bootstrap.sh` 接入；回答詢問或給 `-y`；commit 薄殼與版本鎖定行；升版時 `-y` 只是同意做三方合併，合併後仍有衝突就要手動編輯、再重跑 `upgrade <repo>` 直到乾淨；把契約檢查腳本接進下游 CI", "不需裝引擎的語言環境；不手寫 `gen/`、`cache/`；不改薄殼", "被承諾方：VK 保證不刪、不覆蓋專案檔，失敗必印原因"],
 ["**VK**", "我們，vendor_kit 開發者", "維護引擎與薄殼（含啟動器），履行對兩方的承諾", "不替工具驗可執行；不 commit、不開 PR；引擎不讀 `.git`、不碰 index、不 `git init`", "承諾方：內部怎麼實作不屬於本契約，可自由變更"],
])
Y = para(p1, "p1_trn", Y, M("同一人可兼下游開發者與下游使用者兩種身分。"))
Y = sec(p1, "p1_s3", Y, "兩個自動化角色（不是「方」）")
AUTO = [
 M("下游 CI：專案自己的 CI 平台（GitHub、GitLab 都一樣）只呼叫契約檢查腳本；腳本自己把 `CI` 設為 1 進 CI 模式，依序做同步、驗證、試跑升版、跑工具與專案測試，回第一個失敗步驟的碼。它不寫任何進 git 的檔、不查最新版。"),
 M("Renovate：下游使用者自選的版本更新機器人，用 VK 提供的設定；它開的 PR 只改版本鎖定行，大版本升版分開 PR。初始檔的合併不由它做——下游使用者本機補完再 push。VK 本身沒有機器人。"),
]
AW = 772; ah = max(hv(t, AW) for t in AUTO)
for i, t in enumerate(AUTO):
    p1.append(vb(f"p1_auto{i}", "1", LT12, t, 40 + i * (AW + 16), Y, AW, ah))
Y += ah + 10
# ---- 不變量 I1–I18（一條一格）----
Y = sec(p1, "p1_s4", Y, "不變量")
INVS = [
 "**I1 專案檔四原則**：可以建（明說建了什麼）、要改先問（`-y` 免問）、永不刪、永不覆蓋（不用工具版本取代客製內容）。",
 "**I2 自動化只碰不進 git 的東西**：sync（含工具 recipe 執行前自動觸發的那次）只寫 `cache/`、`gen/`（與執行紀錄）；發現薄殼與引擎不符只以 1 結束並提示跑 `upgrade vendor_kit`，不重寫。",
 "**I3 never fail silently**：失敗一定印原因；需人處理另附可直接複製的下一步指令；warn 也明列條目；印到 tty 的訊息同句進執行紀錄。",
 "**I4 結束碼語意**：0 成功（含 warn）；1 需人處理或失敗；2 合併衝突（留標記、基準版仍推到新版；例外：合併結果是 TOML／just 而解析不過的檔 → 也是 2，但留原檔、該檔基準版不推；update 加 `--exit-code` 時，有新版亦 2）；3 介面版／檔案版不合，須先升級或退回。「回 1 時版本鎖定行不動」適用 add、`upgrade <repo>`、remove、uninstall（寫入前檢查；鎖定行最後才寫／最後才刪）；remove／uninstall 回 1 時留下的狀態 = 該工具仍鎖定、`cache/` 等其餘檔可能部分已刪，進度檔保留、下次可寫動詞先恢復（uninstall 已做完的工具已整個移除、未處理的原樣）；升引擎是唯一例外（引擎那一行已改後才回 1 要求重跑）。多工具動詞的失敗策略依各動詞：upgrade 逐工具做得完的做完；uninstall apply 期間任一工具失敗就中止並列出已完成與未處理的工具；最後都回最需處理的碼（1 > 2 > 0）。",
 "**I5 回 3 零寫入**：除執行紀錄在啟動時已寫下的開頭記錄外完全不寫——不寫專案檔、不寫 `cache/`、`gen/`、進度檔；新舊一律比介面版／檔案版，不比版本字串；最低介面版檢查先於任何上網；網路／認證／不存在回 1，不得偽裝成 3。",
 "**I6 需人處理／失敗語意**：需人處理的結束（1 或 3 且印指令；衝突 2 亦同）為橙；紅只給失敗（拉不到、寫入失敗、驗證失敗）。",
 "**I7 CI 真值規則**：環境變數 `CI` 非空且不為 `0`／`false`（大小寫不敏感）→ CI 模式；契約檢查腳本自己把 `CI` 設為 1；本機手設 = 唯讀驗證，允許。`-y` 與 CI 模式為獨立開關：CI 內可帶 `-y` 省略詢問，但 `-y` 不等於 CI 模式、CI 模式也不隱含 `-y`。CI 模式下升為失敗的警告明列：薄殼不符、基準版落後、未完成接入、任何本機覆寫、需改進 git 的檔；「沒納管／拒絕過」提醒不紅燈；仍拉鎖定版 image、仍寫 `cache/`、`gen/`。唯一例外：`update` 在 CI 模式仍查最新版（它是唯讀動詞，查詢就是它的用途）。",
 "**I8 `-y` 只省略詢問**：不授權覆蓋既有未納管檔、不硬加 append 行、不解除 CI 模式（CI 模式下需改進 git 的檔一律以 1 結束並印清單，與 `-y` 無關）。需詢問但無法互動（無 tty／EOF）又沒給 `-y` → 以 1 結束並印出原因（加 `-y` 或在終端執行）；EOF／Ctrl-C = 中止不套用、不記為拒絕過。",
 "**I9 交付物執行期不依賴 `.vendor_kit/`**：工具 recipe 產生的交付物不得依賴 `.vendor_kit/`、`version.toml`、registry，需要的檔打包時複製進去；初始檔只能引用穩定入口 `just <ns> …`，不得寫死 `cache/` 內部路徑。",
 "**I10 專案根與巢狀**：專案根 = 專案內含 `.vendor_kit/` 的目錄（monorepo 子專案各自一套）；須在某 git repo 內；禁巢狀（install 時上層或下層已有 `.vendor_kit/` → 1）；動詞只准在專案根執行，sync 亦無例外，否則以 1 結束並印出該到哪個目錄執行（工具 recipe 自動觸發的那次 sync 自己先切到專案根，不受影響）。",
 "**I11 進度檔**：所有可寫動詞（含 dev、第一次 install、升引擎）在第一個寫入前必建進度檔，不設例外；可寫動詞開始前遇未完成交易先恢復再繼續（prune 例外：遇活躍進度檔只列出提示、不恢復、不阻擋——它不碰進 git 的檔）；唯讀動詞只偵測不恢復（sync／update 印出未完成交易與恢復指令後以 1 結束，help 印出後仍 0）。",
 "**I12 執行紀錄**：每個動詞每次執行（含 help、沒起容器的 sync、只預覽不寫的執行）及每次 `bootstrap.sh` 執行（寫在 `log/bootstrap/`）必寫一檔。順序：不寫檔、不拉 image、不起容器的前置檢查（是否 git repo、just 版本）可以在建紀錄之前；任何寫入、拉取、起引擎之前必已有紀錄（不是 git 目錄時也無處可寫）；建目錄＋建檔＋寫開頭記錄失敗 → 1、印出無法寫入的原因、零寫入；引擎啟動記錄寫不進亦同；沒有關掉它的選項。",
 "**I13 薄殼人不改**：自描述標頭 hash 不符 → 1 列差異不動；重產只由明確動作（install／`upgrade vendor_kit`）做。",
 "**I14 兩層相容承諾**：救援路徑對任何 ≥ 最低介面版的薄殼永久可用；新版引擎讀歷史 VK 資料永遠可讀、可遷（讀到舊檔案版直接寫成當前檔案版）；舊薄殼呼叫介面版不合的新引擎跑一般動詞，只保證乾淨回 3；最低介面版只能經 ADR 提高。",
 "**I15 檔案版與未知欄位**：VK 寫的每個 TOML 都有檔案版；讀時忽略未知欄位、重寫仍存在的 TOML 時保留未知欄位（不能保留就拒絕寫；uninstall／remove 合法刪掉整個檔或整個工具項目時不適用）；檔案版高於本引擎支援 → 3 零寫入；讀任一舊檔案版直接寫成當前檔案版，不鏈式遷移。",
 "**I16 多工具動詞先完整預檢**：會寫檔且一次處理多個工具的動詞（不帶 `<repo>` 的 upgrade、uninstall）先對全部工具預檢完才動任何東西；任一預檢不過 → 整體不動、以 1 結束並列出原因。預檢過了才開始寫，寫的過程中失敗適用 I4（失敗策略依各動詞、進度檔保留）。",
 "**I17 `gen/tools.just` 與 `cache/` 同次原子替換**：`tools.just` 在同一次寫入裡最後寫，並與 `cache/` 一起原子替換，任何時刻都不會出現「工具入口指向不存在或半套的 cache」。",
 "**I18 版本鎖定行唯一正規形**：形式照第 0 頁「版本鎖定行」：引擎行在頂層 `vendor_kit = \"<image>:<tag>@sha256:<digest>\"`、工具行在 `[tools]` 表下 `<repo> = \"<image>:<tag>@sha256:<digest>\"`——行首無空白、鍵後一個空白、`=`、一個空白、雙引號字串、無尾端註解、LF 結尾；引擎寫出一律此形。`<repo>` 照第 0 頁名稱規則（小寫、不含句點，能作未加引號的 TOML 鍵），與頂層 `schema`／`written_by`／`vendor_kit` 不同層、不撞名。禁 BOM、禁重複鍵、禁 TOML 表旁路寫法（例如 `[tools.<repo>]`、`[vendor_kit]`）；引擎讀到非正規形 → 1 列出差異、不動。",
]
for i, t in enumerate(INVS):
    h = hv(M(t), 1560, pad=4)
    p1.append(vb(f"p1_i{i + 1}", "1", INV, M(t), 40, Y, 1560, h)); Y += h + 4
Y += 6
# ---- 例外清單 ----
Y = sec(p1, "p1_s5", Y, "例外清單（不變量的明文例外）")
EXC = [
 "根 justfile：無 → 建四行（`import '.vendor_kit/entry.just'`、空行、`default:`、`\\t@just --list`）；有 → 問後加 import 一行；uninstall 只刪完全相同的行。",
 "根 `.dockerignore`（I1「永不刪」的明文例外）：install 無則建、有則問後 append 四行（`.vendor_kit/cache/`、`.vendor_kit/gen/`、`.vendor_kit/.tmp.*`、`.vendor_kit/log/`）；只有 uninstall、經詢問、且該行原文仍與 VK 當初寫的相同時，才逐行刪；被改過或缺失的行跳過並 warn。",
 "初始檔換版／三方合併：已納管初始檔經同意（或 `-y`）換新版或三方合併；衝突留標記回 2、基準版推到新版（合併結果是 TOML／just 而解析不過的檔例外：留原檔、該檔基準版不推，也回 2）；`config.toml` 對 `upgrade vendor_kit` 比照。",
 "append 型初始檔：問後加入並記錄實際插入的行；升版只對可辨識的上次插入行提修改；零命中或多處 → 保留只 warn，`-y` 不硬加。",
 "新版刪除的初始檔：只 warn 不刪。",
 "`log/`：VK 檔，不受專案檔四原則；`bootstrap.sh`／第一次 install 失敗清半成品時 `log/` 保留；uninstall 一律保留 `log/`（`.vendor_kit/` 只剩 `log/`）。",
 "進度檔與 `.tmp.*`：同上不受專案檔四原則；成功即刪；prune 遇活躍者只列出提示、不刪、不恢復、不阻擋（I11 的明文例外）。",
 "零寫入的執行紀錄例外：見 I5。",
]
for i, t in enumerate(EXC):
    h = hv(M(t), 1560, pad=4)
    p1.append(vb(f"p1_x{i + 1}", "1", RULE, M(t), 40, Y, 1560, h)); Y += h + 4
Y += 6
# ---- 本頁待拍板 ----
PEND_T = M("**本頁待拍板**\n無；四點已定（2026-09-20）：\n"
 "1. 禁巢狀：install 時上層或下層已有 `.vendor_kit/` 都以 1 結束（I10）。\n"
 "2. 執行位置：動詞只准在專案根執行，sync 亦無例外；自動觸發的那次 sync 自己先切到專案根（I10）。\n"
 "3. `-y` 與 CI 模式是兩個獨立開關：CI 模式下需改進 git 的檔一律以 1 結束並印清單，與 `-y` 無關；`-y` 只省略詢問（I7／I8）。\n"
 "4. 顏色語意：橙 = 需人處理、紅 = 失敗（I6）。\n"
 "其餘三條原列矛盾（零寫入的執行紀錄例外、根 `.dockerignore` 四行、舊薄殼跑介面版不合的新引擎回 3）維持規格所載。規格仍待定的三項（啟動器讀設定檔的方式、外部 repo 反向採用紀錄腳本、紀錄事件名清單待審）不在本頁範圍。")
Y = para(p1, "p1_pend", Y, PEND_T, style=NP_NOTE, pad=10)
c, Y = lgd("p1", 40, Y + 6, ["invb", "ruleb", "tblh", "notep"], "一條不變量一格；出處對照不上圖（見 md）")
p1 += c
pages_v1_a.append(("v1p1", "不變量與角色", p1))
