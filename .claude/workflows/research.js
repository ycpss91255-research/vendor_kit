export const meta = {
  name: 'research',
  description: 'agy 查 → codex 核對 → Claude 整合 → 貼 issue',
  whenToUse: '要找外部前例或資料當決策依據時（例如大型 repo 怎麼設定某件事）；brief 先寫好放在 workspace 的 reference/research/<issue>/',
  phases: [
    { title: '定位', detail: '不論有沒有給 repo，effort low 子代理在 repo（沒給就用工作目錄）跑 git rev-parse --path-format=absolute --git-common-dir，取其上一層當主 repo；腳本與 workspace 一律從主 repo 推' },
    { title: '內部對照', detail: '必跑：一個 Claude 子代理在 repo（沒給就用主 repo）讀已定案資料（01–04、reason_codes.csv、GLOSSARY.md 或 CONTEXT.md、全部 ADR、scope_roadmap.md）、args.issues 指定的 issue 與依關鍵字搜到的相關 issue；每個 brief 回報已定依據（檔名:行號或 issue 留言）、能否只靠既有規則推出、brief 前提與定案的衝突。不存在的檔記下來，不失敗' },
    { title: '調查', detail: '每個 brief 一個 agy（script/workflow/agy_run.py）；內部對照結果寫成 <id>_internal.md 接在 brief 前面當前提；輸出已存在且非空就沿用' },
    { title: '核對', detail: '每份 agy 輸出交給 codex（script/workflow/codex_run.py --delete-brief --reuse，背景執行、逾時預設 2400 秒；JSON 導到 <id>_codex_run.json，前景等待迴圈等它出現），逐條打開來源核對，標正確／有誤／查不到；輸出已存在且非空由 --reuse 沿用；JSON 的 capacity 是 true 時由 JS 再派一次子代理（指令前加 sleep 60），最多重試 2 次' },
    { title: '整合', detail: 'Claude 讀全部 agy 與 codex 輸出與內部對照結果，抽查來源，寫整合結論（先「內部依據」一節，再談外部前例）；internal_basis 不得為空，空的重試一次，仍空就記錯；兩方不一致列成分歧，不選邊' },
    { title: '摘要', detail: '一個 Claude 子代理把整合結論整理成最多 300 字的 issue_summary（結論、分歧、要改的檔，不含本機絕對路徑），JS 檢查長度，超過就重寫一次，再超過就截斷；完整內容留在本機輸出檔' },
    { title: '貼 issue', detail: 'post 為 true 時只貼 issue_summary 一則：子代理把它寫成 <dir>/issue_summary_<ids>.md → script/workflow/prepare_comment.py prepare → script/github/post_comments.py --dir → prepare_comment.py clean；則數與網址由 JS 從兩個 JSON 取並核對' },
  ],
}

// args:
//   issue      number  必填，結果貼到這個 issue
//   topic      string  必填，一句話說明調查目的（給 codex 與 Claude 的背景）
//   briefs     array   必填，每項 { id, label }：brief 檔是 <dir>/<id>_brief.md，agy 輸出 <dir>/<id>_agy.md
//   repo       string  可省，絕對路徑；用來找主 repo：子代理在這裡（沒給就在工作目錄）跑
//                      git rev-parse --path-format=absolute --git-common-dir，取其上一層當主 repo。
//                      腳本一律從 <主 repo>/script/workflow/ 取，workspace＝主 repo 的上一層；
//                      所以 repo 指向沒有新腳本的舊分支 worktree 也不會找錯（#287）。
//                      內部對照也在這裡讀已定案資料（沒給就讀主 repo）；要對照 PR worktree 的檔時明確帶
//   issues     number[] 可省，內部對照一定要讀的已定案 issue 編號（連留言）；另外會依 brief 關鍵字搜相關 issue
//   dir        string  可省，預設 <workspace>/reference/research/<issue>（不放 /tmp）
//   background string  可省，已定案前提
//   post       boolean 可省，預設 true；false 就只產檔不貼 issue
//   agyModel   string  可省，指定 agy 模型名；省略就由 agy_run.py 自動選最新的 gemini flash-high
//   codexTimeout number 可省，codex 核對的逾時秒數（傳給 codex_run.py --timeout），預設 2400；
//                      子代理用 Bash run_in_background 跑，背景上限 7200 秒，所以最多 7000
// 整合輸出寫到 <dir>/claude_review_<id1>[_<id2>…].md（依 briefs 順序串接 id）；
// post 為 true 時只把最多 300 字的 issue_summary 貼成一則留言，完整內容留在本機輸出檔
const { issue, topic, briefs, background = '', post = true, agyModel = '', repo, codexTimeout = 2400, issues = [] } = args ?? {}
if (!Number.isInteger(issue)) throw new Error('args.issue 必填（issue 編號）')
if (typeof topic !== 'string' || !topic.trim()) throw new Error('args.topic 必填')
if (!Array.isArray(briefs) || briefs.length === 0) throw new Error('args.briefs 必填')
if (repo !== undefined && (typeof repo !== 'string' || !repo.trim())) throw new Error('args.repo 必須是 repo 的絕對路徑')
if (!Array.isArray(issues) || issues.some(x => !Number.isInteger(x) || x <= 0)) throw new Error(`args.issues 只能是正整數陣列（收到 ${JSON.stringify(issues)}）`)
// 背景 Bash 的 timeout 上限是 7200000 毫秒，要留 120 秒給 codex_run.py 收尾
if (!Number.isInteger(codexTimeout) || codexTimeout < 1 || codexTimeout > 7000) throw new Error(`args.codexTimeout 必須是 1～7000 的整數秒（收到 ${JSON.stringify(codexTimeout)}）`)
log(`research #${issue}`)

const LOCATE = {
  type: 'object',
  properties: { common_dir: { type: 'string' }, error: { type: 'string' } },
  required: ['common_dir'],
}
const trimDir = x => (typeof x === 'string' ? x.trim().replace(/\/+$/, '') : '')
const repoDir = trimDir(repo)
if (repoDir && !repoDir.startsWith('/')) throw new Error(`args.repo 只能是絕對路徑（收到 ${JSON.stringify(repo)}）；不給就用工作目錄找主 repo`)
// 不論有沒有給 repo 都查 git common dir，取它的上一層當主 repo（在 linked worktree 也會回到主 repo）
const where = repoDir ? `執行 \`git -C ${repoDir} rev-parse --path-format=absolute --git-common-dir\`` : '在目前的工作目錄執行 `git rev-parse --path-format=absolute --git-common-dir`'
const loc = await agent(`只做一件事：${where}，把印出的那一行原樣填進 common_dir。不改任何檔案、不 commit、不 push。指令失敗就把 common_dir 留空、錯誤訊息寫進 error。`,
  { label: `#${issue} 定位 repo`, phase: '定位', schema: LOCATE, effort: 'low' })
const common = trimDir(loc?.common_dir)
if (!common.startsWith('/') || !/\/[^/]+$/.test(common)) throw new Error(`找不到主 repo：${loc?.error || common || '沒有輸出'}${repoDir ? '' : '；請明確帶 args.repo'}`)
const ROOT = common.replace(/\/[^/]+$/, '')
const WS = ROOT.replace(/\/[^/]+$/, '')
const WF = `${ROOT}/script/workflow`
const GH = `${ROOT}/script/github`
log(`research #${issue} main ${ROOT}（腳本 ${WF}、workspace ${WS}）`)
const dir = args.dir ?? `${WS}/reference/research/${issue}`
const REPO = 'ycpss91255-research/vendor_kit'
const BG = background.trim() ? `已定案前提（不要質疑）：\n${background.trim()}\n` : ''
const brief = b => `${dir}/${b.id}_brief.md`
const agyOut = b => `${dir}/${b.id}_agy.md`
const codexOut = b => `${dir}/${b.id}_codex.md`
const codexBrief = b => `${dir}/${b.id}_codex_brief.md`
// 背景 codex_run.py 的 stdout JSON 導到這個檔，子代理用前景等待迴圈等它出現（#302）
const runJson = b => `${dir}/${b.id}_codex_run.json`
// 整合輸出帶 brief id，同一 issue 換一批 brief 再跑不會覆蓋前一次
const claudeOut = `${dir}/claude_review_${briefs.map(b => b.id).join('_')}.md`
const MODEL = agyModel.trim() ? ` --model ${agyModel.trim()}` : ''
// 內部對照讀哪份檔：給了 repo 就讀它（可以是 PR worktree），沒給就讀主 repo
const SRC = repoDir || ROOT
log(`research #${issue} 內部對照讀 ${SRC}`)

// 內部對照（#359）：任何外部調查之前，先把已定案資料對照到每個 brief。
// agy、codex 與 Claude 整合都拿到同一份，當作不可質疑的前提；先引用內部依據再談外部前例。
const SEARCH_LIMIT = 5 // 依關鍵字搜相關 issue 時，每個 brief 最多讀幾個
const PAGES = ['01_purpose.md', '02_invariants.md', '03_output.md', '04_interface.md']
const BASIS_ITEM = {
  type: 'object',
  properties: {
    source: { type: 'string', description: '出處：repo 相對檔名:行號，或 #<issue> 本文／#<issue> 留言（作者、日期）' },
    says: { type: 'string', description: '這個出處說了什麼，一句話' },
  },
  required: ['source', 'says'],
}
const INTERNAL = {
  type: 'object',
  properties: {
    items: {
      type: 'array',
      description: '每個 brief 一項，id 對應 brief 的 id',
      items: {
        type: 'object',
        properties: {
          id: { type: 'string' },
          basis: { type: 'array', items: BASIS_ITEM, description: '跟這個 brief 有關的已定依據；找不到就給空陣列，不要編' },
          derivable: { type: 'boolean', description: '這個 brief 要回答的問題能否只靠既有規則推出答案，不需要外部前例或新的決定' },
          derived_answer: { type: 'string', description: 'derivable 為 true 時必填：推出的答案與推導（引用 basis 的出處）；false 時留空' },
          conflicts: { type: 'array', items: { type: 'string' }, description: 'brief 的前提或描述與已定案內容衝突之處（附出處）；沒有就空陣列' },
        },
        required: ['id', 'basis', 'derivable', 'derived_answer', 'conflicts'],
      },
    },
    read: { type: 'array', items: { type: 'string' }, description: '實際讀到的檔（repo 相對路徑）與 issue（#N）' },
    missing: { type: 'array', items: { type: 'string' }, description: '嘗試過但不存在的路徑（每個候選都記）' },
    error: { type: 'string', description: '失敗原因；成功留空' },
  },
  required: ['items', 'read', 'missing'],
}
phase('內部對照')
const bList = briefs.map(b => `- id: ${b.id}（${b.label}）：brief 檔 ${brief(b)}`).join('\n')
const internal = await agent(`只讀，不要改任何檔、不要發 issue 或留言。你的工作是在外部調查開始前，把已定案的內部資料對照到每個 brief。

調查目的：${topic}
${BG}
repo 根目錄：${SRC}（以下路徑都相對於它）

先讀每個 brief 檔，弄清楚它要查什麼：
${bList}

再依序讀這些已定案資料；候選路徑照順序試，第一個存在的就用，不存在的每個都記進 missing，不要因此失敗：
1. 對外契約頁，每頁先試 doc/contract/<頁>，找不到再試 doc/decisions/review/<頁>；頁：${PAGES.join('、')}
2. doc/contract/reason_codes.csv
3. 名詞：根目錄 GLOSSARY.md，找不到再試 CONTEXT.md
4. doc/adr/*.md 全部（README.md 也讀，它是規則）
5. scope_roadmap.md：用 \`find ${SRC} -name scope_roadmap.md -not -path '*/node_modules/*' -not -path '*/.git/*'\` 找，全部讀
6. 已定案 issue：${issues.length ? issues.map(n => `\`gh issue view ${n} -R ${REPO} --comments\``).join('、') : '（args.issues 沒給）'}
7. 相關 issue：每個 brief 取兩三個關鍵字跑 \`gh search issues "<關鍵字>" -R ${REPO} --limit ${SEARCH_LIMIT} --json number,title,state\`，每個 brief 最多讀 ${SEARCH_LIMIT} 個看起來相關的（\`gh issue view <N> -R ${REPO} --comments\`）；issue 本文開好後不改，新決定在留言，兩者都要看

對每個 brief 回報一項（id 照抄）：
- basis：跟這個 brief 有關的已定依據，每項 { source, says }。source 用 repo 相對檔名:行號（例如 doc/decisions/review/02_invariants.md:42），或 #<issue> 本文／#<issue> 留言（作者、日期）；says 一句話。只列真的讀到的，不要編、不要寫本機絕對路徑。
- derivable：只靠上面的既有規則就能回答 brief 要查的問題、不需要外部前例或新的決定（也不改對外承諾）時填 true；要外部資料、新的取捨、規則沒涵蓋或規則彼此衝突時填 false。
- derived_answer：derivable 為 true 時必填，寫推出的答案與推導，引用 basis 的出處；false 時留空字串。
- conflicts：brief 的前提或描述與已定案內容衝突就列出（附出處），沒有就空陣列。

read 列實際讀到的檔與 issue，missing 列嘗試過但不存在的路徑。整個對照做不下去（例如 repo 不存在）才填 error。`,
  { label: `#${issue} 內部對照`, phase: '內部對照', schema: INTERNAL })
if (!internal || (internal.error && !(Array.isArray(internal.items) && internal.items.length))) {
  throw new Error(`內部對照失敗：${internal?.error || '子代理沒有回報'}`)
}
const strs = xs => (Array.isArray(xs) ? xs.filter(x => typeof x === 'string' && x.trim()).map(x => x.trim()) : [])
const basisOf = new Map()
for (const b of briefs) {
  const x = (Array.isArray(internal.items) ? internal.items : []).find(i => i && i.id === b.id)
  if (!x) log(`research #${issue} 內部對照沒有回報 ${b.id}，當作沒有依據、不可由規則推出`)
  const basis = (Array.isArray(x?.basis) ? x.basis : [])
    .filter(y => y && typeof y.source === 'string' && y.source.trim())
    .map(y => ({ source: y.source.trim(), says: typeof y.says === 'string' ? y.says.trim() : '' }))
  const derived_answer = typeof x?.derived_answer === 'string' ? x.derived_answer.trim() : ''
  let derivable = x?.derivable === true
  if (derivable && (!derived_answer || basis.length === 0)) {
    log(`research #${issue} ${b.id} 標了可由規則推出但沒有 derived_answer 或 basis，改當不可推出`)
    derivable = false
  }
  basisOf.set(b.id, { id: b.id, basis, derivable, derived_answer: derivable ? derived_answer : '', conflicts: strs(x?.conflicts) })
}
log(`research #${issue} 內部對照：讀到 ${strs(internal.read).length} 份，不存在 ${strs(internal.missing).length} 個，可由規則推出 ${[...basisOf.values()].filter(x => x.derivable).length} 份`)

// 內部對照的結果：agy、codex 與 Claude 整合都拿到同一份，當作不可質疑的前提
const basisText = b => {
  const x = basisOf.get(b.id)
  const lines = x.basis.length
    ? x.basis.map(y => `- ${y.source}：${y.says}`).join('\n')
    : '- （內部對照沒有找到這個 brief 的依據）'
  const derived = x.derivable
    ? `內部對照判定：這題可由既有規則推出，推出的答案：${x.derived_answer}\n外部資料要推翻它，必須指出哪條依據讀錯或不適用，並附證據。`
    : '內部對照判定：這題不能只靠既有規則推出。'
  const conflicts = x.conflicts.length ? `\nbrief 前提與已定案內容的衝突：\n${x.conflicts.map(y => `- ${y}`).join('\n')}` : ''
  return `內部依據（已定案資料，由「內部對照」階段整理；這是不可質疑的前提）：
${lines}
${derived}${conflicts}

先引用內部依據，再談外部前例；外部做法與內部依據衝突時要明講是哪一條，不要用外部前例推翻已定案內容。`
}
// agy 的前提檔：接在原 brief 前面，合成 <id>_agy_brief.md 再交給 agy_run.py
const internalFile = b => `${dir}/${b.id}_internal.md`
const agyBrief = b => `${dir}/${b.id}_agy_brief.md`

const RUN = {
  type: 'object',
  properties: { exit: { type: 'integer' }, out_ok: { type: 'boolean' }, reused: { type: 'boolean' }, model: { type: 'string' }, error: { type: 'string' } },
  required: ['exit', 'out_ok'],
}
// codex 核對的子代理每次只跑一次 codex_run.py，照抄它 JSON 的欄位；要不要重試由 JS 判斷
const CODEX_ATTEMPT = {
  type: 'object',
  properties: {
    ok: { type: 'boolean' }, exit: { type: 'integer' }, reused: { type: 'boolean' }, timed_out: { type: 'boolean' },
    capacity: { type: 'boolean' }, error: { type: 'string' }, stderr_tail: { type: 'string' },
  },
  required: ['ok', 'exit', 'reused', 'timed_out', 'capacity'],
}
// 背景 Bash 的 timeout（毫秒）：codex 逾時再加 120 秒，讓 codex_run.py 砍掉 codex 後還來得及印 JSON
const BG_TIMEOUT_MS = (codexTimeout + 120) * 1000
const CAPACITY_WAIT_S = 60
const CAPACITY_RETRIES = 2
// 前景等待迴圈：一輪 590 秒（前景 Bash 上限 600 秒，留 10 秒給 test 與 echo），
// 總等待涵蓋 codex 逾時加收尾 120 秒；capacity 重試另加等待的秒數（#302）
const WAIT_ROUND_S = 590
const WAIT_ROUNDS = Math.ceil((codexTimeout + 120) / WAIT_ROUND_S)
const RETRY_WAIT_ROUNDS = Math.ceil((codexTimeout + 120 + CAPACITY_WAIT_S) / WAIT_ROUND_S)
const waitCmd = b => `timeout ${WAIT_ROUND_S} sh -c 'until [ -s ${runJson(b)} ]; do sleep 15; done'; test -s ${runJson(b)} && echo ready || echo waiting`

const codexRun = b => `python3 ${WF}/codex_run.py --cd ${dir} --brief ${codexBrief(b)} --out ${codexOut(b)} --timeout ${codexTimeout} --delete-brief --reuse`
// 核對子代理的指示；retry 時背景指令前加 sleep，背景 timeout 與等待次數多算等待的秒數
const codexPrompt = (b, retry) => {
  const bg = `${retry ? `sleep ${CAPACITY_WAIT_S}; ` : ''}${codexRun(b)} > ${runJson(b)} 2>&1`
  const bgTimeout = BG_TIMEOUT_MS + (retry ? CAPACITY_WAIT_S * 1000 : 0)
  const rounds = retry ? RETRY_WAIT_ROUNDS : WAIT_ROUNDS
  return `你的工作是用腳本啟動 codex 核對 agy 的調查結果，**你自己不核對、不加意見、不判斷要不要重試**。不改任何 repo、不 commit、不 push。每一步都照做，不要自己先檢查輸出檔在不在（沿用由腳本的 --reuse 判斷）。

1. 用 Write 工具把下面的 brief 原文寫進 ${codexBrief(b)}（不要用 heredoc）：
---
${BG}調查目的：${topic}

${basisText(b)}

讀 ${agyOut(b)}（agy 的調查輸出）與它的題目 ${brief(b)}。第一節「內部依據」：列出上面跟這題有關的內部依據（出處：一句話），並指出 agy 的結論有沒有與它衝突、衝突在哪。接著逐條打開 agy 引用的來源（網址、workflow 檔、文件）核對：每條標「正確／有誤／查不到來源」，有誤就寫出正確內容與來源網址。agy 漏掉的重要事實自己補上，同樣附來源。最後一節「核對後結論」：先引用內部依據，再依核對結果寫修正後的外部前例結論與數量統計。用繁體中文 markdown，不要改任何檔。
---
2. 先清掉上一次的結果檔，前景執行一次（指令一字不差）：
   \`rm -f ${runJson(b)}\`
   再用 Bash 的 run_in_background 執行（timeout ${bgTimeout}），指令一字不差（JSON 導到結果檔）：
   \`${bg}\`
   **codex 本身不要用前景執行**：前景 Bash 上限 600 秒，codex 逐條核對大份調查會超過。
3. 啟動後馬上用**前景** Bash（timeout 600000）跑等待迴圈，指令一字不差：
   \`${waitCmd(b)}\`
   印 waiting 就再跑同一個指令；印 ready 就往下做。最多跑 ${rounds} 次等待迴圈（總共約 ${rounds * WAIT_ROUND_S} 秒，涵蓋 codex 逾時 ${codexTimeout} 秒加收尾 120 秒${retry ? `與等待的 ${CAPACITY_WAIT_S} 秒` : ''}）；跑滿還是 waiting 就算逾時：回報 ok false、exit -1、reused false、timed_out true、capacity false，error 寫「等待 codex_run.py 結果逾時」，再做第 5 步的刪檔。
   **只能這樣等**：不要用 Monitor（repo 的 monitor_guard hook 會擋）、不要單獨跑 sleep、不要只等背景通知就先輸出回報（背景工作會在你回報時被砍，codex 輸出就沒了）。
4. 用 Read 讀 ${runJson(b)}，裡面是 codex_run.py 印出的那一行 JSON。內容不是一行 JSON（例如腳本本身報錯）就回報 ok false、exit -1、reused false、timed_out false、capacity false，error 附檔案內容。
5. 結束前（成功、失敗、逾時都一樣）前景執行一次 \`rm -f ${runJson(b)}\`。
6. 依 JSON 照實回報：ok、reused、timed_out、capacity、error、stderr_tail 照抄 JSON 的同名欄位（error 是 null 就留空）；exit＝JSON 的 exit，是 null（逾時、沿用或沒跑起來）時：ok 是 true 回報 0，否則回報 -1。不要自己看 shell 的結束碼或 codex 的輸出檔，不要重跑。`
}

const results = await pipeline(
  briefs,
  b => agent(`你的工作是用腳本執行 agy 做資料調查，**你自己不調查、不改寫輸出**。不改任何 repo、不 commit、不 push。

1. 用 Write 工具把下面 --- 之間的前提原文寫進 ${internalFile(b)}（不要用 heredoc、不要改字）：
---
${BG}調查目的：${topic}

${basisText(b)}

調查輸出的第一節寫「內部依據」：列出上面跟這題有關的內部依據（出處：一句話）；接著才是外部前例與資料，每條附來源。外部做法與內部依據衝突時要明講。

以下是調查題目原文：

---
2. 前景執行一次，指令一字不差（把前提與原 brief 合成交給 agy 的 brief）：
   \`cat ${internalFile(b)} ${brief(b)} > ${agyBrief(b)}\`
3. 前景執行（Bash timeout 600000），指令一字不差：
   \`python3 ${WF}/agy_run.py --cd ${dir} --brief ${agyBrief(b)} --out ${agyOut(b)} --err ${dir}/${b.id}_agy.err${MODEL}\`
   跑不完就用 run_in_background 重跑同一行並等它結束，不要中途放棄（腳本先寫 .part、成功才改名，不會沿用半成品）。輸出已存在且非空時腳本會直接沿用。
4. 讀它印出的那一行 JSON，照實回報：exit＝JSON 的 exit、out_ok＝JSON 的 ok、reused＝JSON 的 reused、model＝JSON 的 model（沿用時可能是空的）；ok 是 false 就把 JSON 的 error 與 err_tail 寫進 error。不要自己判斷輸出檔、不要自己刪 .err。`,
    { label: `#${issue} agy:${b.id}`, phase: '調查', schema: RUN }),
  async (r, b) => {
    if (!r || r.exit !== 0 || !r.out_ok) return { b, agy: r, codex: null }
    // at capacity 的重試由 JS 決定：每次派一個新的子代理，各自是單獨的背景指令（背景上限 7200 秒）
    let last = null
    let attempts = 0
    for (let i = 0; i <= CAPACITY_RETRIES; i++) {
      attempts = i + 1
      last = await agent(codexPrompt(b, i > 0),
        { label: `#${issue} codex:${b.id}${i > 0 ? ` 重試 ${i}` : ''}`, phase: '核對', schema: CODEX_ATTEMPT })
      if (!last || last.ok || !last.capacity || last.timed_out) break
      if (i < CAPACITY_RETRIES) log(`codex:${b.id} at capacity，${CAPACITY_WAIT_S} 秒後重試（第 ${i + 1} 次）`)
    }
    const codex = last
      ? {
          exit: last.exit, out_ok: last.ok, reused: !!last.reused, timed_out: !!last.timed_out,
          capacity: !!last.capacity, attempts,
          ...(last.ok ? {} : { error: [last.error, last.stderr_tail].filter(Boolean).join('\n') }),
        }
      : { exit: -1, out_ok: false, reused: false, timed_out: false, capacity: false, attempts, error: 'codex 核對的子代理沒有回傳結果' }
    return { b, agy: r, codex }
  },
)

const ok = results.filter(x => x && x.codex && x.codex.exit === 0 && x.codex.out_ok)
const failed = results.filter(x => !ok.includes(x)).map(x => ({ id: x?.b?.id, agy: x?.agy, codex: x?.codex }))
if (failed.length) log(`未完成：${failed.map(f => f.id).join('、')}`)
const internalOut = { read: strs(internal.read), missing: strs(internal.missing), items: [...basisOf.values()] }
if (!ok.length) return { failed, internal: internalOut }

phase('整合')
// 整合輸出必填 internal_basis：空的視為無效，重試一次，仍空就記錯
const REVIEW = {
  type: 'object',
  properties: {
    output_file: { type: 'string' },
    internal_basis: { type: 'array', items: { type: 'string' }, description: '整合結論引用的內部依據，每條「出處（repo 相對檔名:行號或 #issue 留言）：一句話」；不得為空' },
    summary: { type: 'string' },
    error: { type: 'string' },
  },
  required: ['output_file', 'internal_basis', 'summary'],
}
const reviewPrompt = retry => `你負責整合外部調查的結果。不改任何 repo、不 commit、不 push、不發 issue。

${BG}調查目的：${topic}
資料（每組是 agy 調查與 codex 核對）：
${ok.map(x => `- ${x.b.label}：${agyOut(x.b)}、${codexOut(x.b)}`).join('\n')}

每組的內部依據（由「內部對照」階段整理，是不可質疑的前提）：
${ok.map(x => `### ${x.b.label}（${x.b.id}）\n\n${basisText(x.b)}`).join('\n\n')}

做法：
1. 兩份都讀。codex 標「有誤」或兩者說法不同的地方，自己打開來源抽查（WebFetch），以來源為準。
2. 整合結論的第一節是「內部依據」：每組列出引用的內部依據（出處：一句話），標明外部結果與它一致或衝突；內部對照判定可由既有規則推出的組，寫出推出的答案，外部資料沒有推翻它就以它為準。
3. 接著寫外部前例：每組的主流做法與數量（以核對後的結果為準），各自附代表 repo 與來源連結；組與組之間的差異；對「調查目的」的意涵。先引用內部依據再談外部前例，外部前例不能推翻已定案內容，衝突要明講是哪一條。
4. agy、codex 與你的判斷不一致、而來源無法判定的，列在「分歧」一節，各方立場都寫，不替任何一方下定論。
5. 沒有來源的主張標明是推論。

用繁體中文 markdown 寫到 ${claudeOut}，回報 output_file、internal_basis（「內部依據」一節引用的每條「出處：一句話」，不得為空）與 summary（結論一節的全文）。${retry ? '\n\n你上一次的回報 internal_basis 是空的，被判為無效。這次「內部依據」一節與 internal_basis 都必須列出內部依據；確實沒有相關條文時，寫明查過哪些檔（出處）與「沒有相關條文」。' : ''}`
const errors = []
let review = await agent(reviewPrompt(false), { label: `#${issue} Claude 整合`, phase: '整合', schema: REVIEW })
if (review && !review.error && strs(review.internal_basis).length === 0) {
  log(`research #${issue} 整合沒有引用內部依據，重試一次`)
  review = await agent(reviewPrompt(true), { label: `#${issue} Claude 整合 重試`, phase: '整合', schema: REVIEW })
}
if (review && !review.error && strs(review.internal_basis).length === 0) {
  review = { ...review, error: '整合的 internal_basis 為空（重試一次仍空），結論無效' }
}
if (!review) errors.push('整合的子代理沒有回傳結果')
else if (review.error) errors.push(`整合：${review.error}`)
// 整合無效就不摘要、不貼 issue
if (!review || review.error) return { ok: ok.map(x => x.b.id), failed, review, internal: internalOut, errors }

// issue_summary：貼 issue 用，最多 SUMMARY_MAX 字（中文一字算一，標點空白也算），不含本機絕對路徑。
// 超過或含本機路徑就重寫一次；再不行就把路徑換掉、截斷並加 TRUNC（規則同 discuss）
phase('摘要')
const SUMMARY_MAX = 300
const TRUNC = '…（完整內容見本機輸出檔）'
const len = s => Array.from(s).length
const ABS_PATH = /(^|[^\w.~-])\/(home|tmp|Users|root|mnt|media|var|opt|private)\/[^\s`'"）)]*/g
const relLocal = s => [SRC, ROOT].reduce((t, d) => t.split(`${d}/`).join('').split(d).join('.'), String(s ?? '').trim())
const hasAbs = s => new RegExp(ABS_PATH.source).test(s)
const summaryProblems = s => [
  ...(!s ? ['摘要是空的'] : []),
  ...(len(s) > SUMMARY_MAX ? [`長度 ${len(s)} 字，超過上限 ${SUMMARY_MAX}`] : []),
  ...(hasAbs(s) ? ['含本機絕對路徑'] : []),
]
const compact = {
  topic,
  conclusion: review.summary,
  internal_basis: strs(review.internal_basis),
  by_rule: [...basisOf.values()].filter(x => x.derivable).map(x => ({ id: x.id, derived_answer: x.derived_answer })),
  conflicts: [...basisOf.values()].filter(x => x.conflicts.length).map(x => ({ id: x.id, conflicts: x.conflicts })),
  failed: failed.map(f => f.id),
}
const SUMMARY = {
  type: 'object',
  properties: {
    summary: { type: 'string', description: `issue 摘要，最多 ${SUMMARY_MAX} 字` },
    error: { type: 'string', description: '失敗原因；成功留空' },
  },
  required: ['summary'],
}
const summarize = (prev, problems) => agent(`把下面的調查結果整理成貼 issue 用的摘要。只整理，不要加入新的立場、不要跑 gh。需要細節時可以讀 ${claudeOut}（整合結論全文），不要改任何檔。

規則：
- 最多 ${SUMMARY_MAX} 個字元（中文一字算一，英數、標點、空白、換行也各算一）。
- 內容：結論（先內部依據再外部前例）、分歧點、要改的檔（repo 相對路徑）；可由既有規則推出的標明「依規則定」。
- 不含本機絕對路徑（例如 /home/...）；提到檔案一律用 repo 相對路徑。
- 不要客套話、不要標題層級，用短條列。

調查結果：
${JSON.stringify(compact)}${prev ? `

你上一版摘要不合格（${problems.join('；')}），請重寫：
${prev}` : ''}`,
  { label: `#${issue} 摘要${prev ? ' 重寫' : ''}`, phase: '摘要', schema: SUMMARY })
let issue_summary = relLocal((await summarize())?.summary)
let problems = summaryProblems(issue_summary)
if (problems.length) {
  log(`research #${issue} 摘要不合格（${problems.join('；')}），重寫一次`)
  const again = relLocal((await summarize(issue_summary || '（空）', problems))?.summary)
  if (again) issue_summary = again
  problems = summaryProblems(issue_summary)
}
if (!issue_summary) {
  // 摘要子代理兩次都沒有結果：由腳本組最小摘要，避免貼出空字串
  issue_summary = `- ${topic}：完整結論見本機輸出檔`
  errors.push('摘要子代理沒有回報，issue_summary 由腳本組成')
}
if (hasAbs(issue_summary)) issue_summary = issue_summary.replace(ABS_PATH, (all, pre) => `${pre}<本機路徑>`)
if (len(issue_summary) > SUMMARY_MAX) {
  log(`research #${issue} 摘要重寫後仍有 ${len(issue_summary)} 字，截斷`)
  issue_summary = Array.from(issue_summary).slice(0, SUMMARY_MAX - len(TRUNC)).join('') + TRUNC
}

const base = { ok: ok.map(x => x.b.id), failed, summary: review.summary, review_file: review.output_file, issue_summary, internal: internalOut, errors }
if (!post) return base

phase('貼 issue')
// 只貼 issue_summary 一則；agy、codex 原文與整合全文留在本機輸出檔。
// 留言檔的標記、本機路徑替換與自檢由 prepare_comment.py 做；
// 貼出由 post_comments.py 做，每則寫入前都把同一個 argv 交給 .claude/settings.json 註冊的 Bash hook 檢查
const POST_DIR = `${dir}/post`
const summaryFile = `${dir}/issue_summary_${briefs.map(b => b.id).join('_')}.md`
// 標題用單引號包，bash 與 fish 都照字面讀；單引號與反斜線先換掉
const q = s => `'${String(s).replace(/'/g, '’').replace(/\\/g, '/')}'`
const items = `--item claude ${summaryFile} ${q(`${topic.trim()} 調查摘要`)}`
const POSTED = {
  type: 'object',
  properties: {
    prepare_ok: { type: 'boolean' }, files: { type: 'integer' }, problems: { type: 'string' },
    post_json: { type: 'string' }, clean_ok: { type: 'boolean' }, error: { type: 'string' },
  },
  required: ['prepare_ok', 'files', 'post_json'],
}
const posted = await agent(`把調查摘要貼到 GitHub issue #${issue}（repo ${REPO}）。不改 repo、不 commit。留言檔的準備與貼出都由腳本做，你只照順序做下面四步、照抄腳本的輸出；不要自己加標記、換路徑、切分或改留言檔，也不要自己下任何 gh 指令。

1. 用 Write 工具把下面 --- 之間的摘要原文寫進 ${summaryFile}（不要用 heredoc、一個字都不要改）：
---
${issue_summary}
---
2. 執行一次（指令一字不差）：
   \`python3 ${WF}/prepare_comment.py prepare --out-dir ${POST_DIR} --workspace ${WS} ${items}\`
   讀它印出的 JSON：prepare_ok＝JSON 的 ok、files＝JSON 的 files 陣列長度；ok 是 false 就把 problems 原樣寫進 problems，跳過第 3 步（post_json 留空），直接做第 4 步。
3. 執行一次（指令一字不差，不要拆成逐則、不要加旗標）：
   \`python3 ${GH}/post_comments.py --kind issue --number ${issue} --dir ${POST_DIR}\`
   把它印出的那一行 JSON 原樣填進 post_json（結束碼不是 0 也照填，不要重跑、不要自己補貼）。沒有印出 JSON 就把輸出原樣寫進 error。
4. 最後執行一次 \`python3 ${WF}/prepare_comment.py clean --out-dir ${POST_DIR}\`（前面失敗也要跑），clean_ok＝JSON 的 ok。`,
  { label: `#${issue} 貼 issue`, phase: '貼 issue', schema: POSTED })

// 則數取 prepare 的 files（摘要只有一則），網址取 post_comments 的 urls
let postRes = null
let postError = ''
if (posted?.post_json?.trim()) {
  try { postRes = JSON.parse(posted.post_json.trim()) } catch { postError = `post_comments.py 的輸出不是 JSON：${posted.post_json.trim().slice(0, 500)}` }
}
const urls = Array.isArray(postRes?.urls) ? postRes.urls : []
const planned = posted?.prepare_ok ? (posted.files ?? 0) : 0
if (!posted) postError = '貼 issue 的子代理沒有回傳結果'
else if (!posted.prepare_ok) postError = `prepare_comment.py 準備留言檔失敗：${posted.problems || posted.error || '沒有說明'}`
else if (planned < 1) postError = '沒有準備出任何留言檔（planned 為 0）'
else if (planned > 1) postError = `摘要應該只有 1 則，prepare_comment.py 切成 ${planned} 則`
else if (!postError && !postRes) postError = `post_comments.py 沒有輸出 JSON${posted.error ? `：${posted.error}` : ''}`
else if (postRes && !postRes.ok) {
  const why = [postRes.error, postRes.failed_at && `停在 ${postRes.failed_at}`, postRes.denied?.length && `hook 擋下：${JSON.stringify(postRes.denied)}`].filter(Boolean).join('；')
  postError = `post_comments.py 失敗：${why || '沒有說明'}`
}
if (posted && planned >= 1 && urls.length !== planned) {
  const diff = planned - urls.length
  const msg = `預計 ${planned} 則，實際貼出 ${urls.length} 則，${diff > 0 ? `少了 ${diff}` : `多了 ${-diff}`} 則`
  log(`貼 issue 不齊：${msg}`)
  postError = postError ? `${msg}；${postError}` : msg
}
if (posted && posted.clean_ok === false) postError = postError ? `${postError}；prepare_comment.py clean 失敗` : 'prepare_comment.py clean 失敗'
const out = { ...base, planned, urls }
if (postError) out.error = postError
return out

// args 範例：
// {
//   "issue": 140,
//   "topic": "<一句話說明調查目的>",
//   "background": "<已定案前提>",
//   "issues": [78],
//   "briefs": [
//     { "id": "ros", "label": "ROS 生態系" },
//     { "id": "ubuntu", "label": "Canonical／Ubuntu" }
//   ]
// }
