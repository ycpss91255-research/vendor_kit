export const meta = {
  name: 'research',
  description: 'agy 查 → codex 核對 → Claude 整合 → 貼 issue',
  whenToUse: '要找外部前例或資料當決策依據時（例如大型 repo 怎麼設定某件事）；brief 先寫好放在 workspace 的 reference/research/<issue>/',
  phases: [
    { title: '定位', detail: '不論有沒有給 repo，effort low 子代理在 repo（沒給就用工作目錄）跑 git rev-parse --path-format=absolute --git-common-dir，取其上一層當主 repo；腳本與 workspace 一律從主 repo 推' },
    { title: '調查', detail: '每個 brief 一個 agy（script/workflow/agy_run.py）；輸出已存在且非空就沿用' },
    { title: '核對', detail: '每份 agy 輸出交給 codex（script/workflow/codex_run.py，背景執行、逾時預設 2400 秒），逐條打開來源核對，標正確／有誤／查不到；輸出已存在且非空就沿用，model at capacity 時等 60 秒重試最多 2 次' },
    { title: '整合', detail: 'Claude 讀全部 agy 與 codex 輸出，抽查來源，寫整合結論；兩方不一致列成分歧，不選邊' },
    { title: '貼 issue', detail: 'script/workflow/prepare_comment.py 準備留言檔，依序貼 [agy] 原文、[codex] 原文、[claude] 整合結論，核對則數' },
  ],
}

// args:
//   issue      number  必填，結果貼到這個 issue
//   topic      string  必填，一句話說明調查目的（給 codex 與 Claude 的背景）
//   briefs     array   必填，每項 { id, label }：brief 檔是 <dir>/<id>_brief.md，agy 輸出 <dir>/<id>_agy.md
//   repo       string  可省，絕對路徑；只用來找主 repo：子代理在這裡（沒給就在工作目錄）跑
//                      git rev-parse --path-format=absolute --git-common-dir，取其上一層當主 repo。
//                      腳本一律從 <主 repo>/script/workflow/ 取，workspace＝主 repo 的上一層；
//                      所以 repo 指向沒有新腳本的舊分支 worktree 也不會找錯（#287）
//   dir        string  可省，預設 <workspace>/reference/research/<issue>（不放 /tmp）
//   background string  可省，已定案前提
//   post       boolean 可省，預設 true；false 就只產檔不貼 issue
//   agyModel   string  可省，指定 agy 模型名；省略就由 agy_run.py 自動選最新的 gemini flash-high
//   codexTimeout number 可省，codex 核對的逾時秒數（傳給 codex_run.py --timeout），預設 2400；
//                      子代理用 Bash run_in_background 跑，背景上限 7200 秒，所以最多 7000
// 整合輸出寫到 <dir>/claude_review_<id1>[_<id2>…].md（依 briefs 順序串接 id）
const { issue, topic, briefs, background = '', post = true, agyModel = '', repo, codexTimeout = 2400 } = args ?? {}
if (!Number.isInteger(issue)) throw new Error('args.issue 必填（issue 編號）')
if (typeof topic !== 'string' || !topic.trim()) throw new Error('args.topic 必填')
if (!Array.isArray(briefs) || briefs.length === 0) throw new Error('args.briefs 必填')
if (repo !== undefined && (typeof repo !== 'string' || !repo.trim())) throw new Error('args.repo 必須是 repo 的絕對路徑')
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
log(`research #${issue} main ${ROOT}（腳本 ${WF}、workspace ${WS}）`)
const dir = args.dir ?? `${WS}/reference/research/${issue}`
const REPO = 'ycpss91255-research/vendor_kit'
const BG = background.trim() ? `已定案前提（不要質疑）：\n${background.trim()}\n` : ''
const brief = b => `${dir}/${b.id}_brief.md`
const agyOut = b => `${dir}/${b.id}_agy.md`
const codexOut = b => `${dir}/${b.id}_codex.md`
const codexBrief = b => `${dir}/${b.id}_codex_brief.md`
// 整合輸出帶 brief id，同一 issue 換一批 brief 再跑不會覆蓋前一次
const claudeOut = `${dir}/claude_review_${briefs.map(b => b.id).join('_')}.md`
const MODEL = agyModel.trim() ? ` --model ${agyModel.trim()}` : ''

const RUN = {
  type: 'object',
  properties: { exit: { type: 'integer' }, out_ok: { type: 'boolean' }, reused: { type: 'boolean' }, model: { type: 'string' }, error: { type: 'string' } },
  required: ['exit', 'out_ok'],
}
// codex 核對另外回報跑了幾次與最後一次是否逾時
const CODEX_RUN = {
  type: 'object',
  properties: { ...RUN.properties, attempts: { type: 'integer' }, timed_out: { type: 'boolean' } },
  required: ['exit', 'out_ok', 'reused', 'attempts'],
}
// 背景 Bash 的 timeout（毫秒）：codex 逾時再加 120 秒，讓 codex_run.py 砍掉 codex 後還來得及印 JSON
const BG_TIMEOUT_MS = (codexTimeout + 120) * 1000
const CAPACITY_WAIT_S = 60
const CAPACITY_RETRIES = 2

const results = await pipeline(
  briefs,
  b => agent(`你的工作是用腳本執行 agy 做資料調查，**你自己不調查、不改寫輸出**。不改任何 repo、不 commit、不 push。

1. 前景執行（Bash timeout 600000），指令一字不差：
   \`python3 ${WF}/agy_run.py --cd ${dir} --brief ${brief(b)} --out ${agyOut(b)} --err ${dir}/${b.id}_agy.err${MODEL}\`
   跑不完就用 run_in_background 重跑同一行並等它結束，不要中途放棄（腳本先寫 .part、成功才改名，不會沿用半成品）。輸出已存在且非空時腳本會直接沿用。
2. 讀它印出的那一行 JSON，照實回報：exit＝JSON 的 exit、out_ok＝JSON 的 ok、reused＝JSON 的 reused、model＝JSON 的 model（沿用時可能是空的）；ok 是 false 就把 JSON 的 error 與 err_tail 寫進 error。不要自己判斷輸出檔、不要自己刪 .err。`,
    { label: `#${issue} agy:${b.id}`, phase: '調查', schema: RUN }),
  (r, b) => {
    if (!r || r.exit !== 0 || !r.out_ok) return { b, agy: r, codex: null }
    const run = `python3 ${WF}/codex_run.py --cd ${dir} --brief ${codexBrief(b)} --out ${codexOut(b)} --timeout ${codexTimeout} --delete-brief`
    return agent(`你的工作是用腳本啟動 codex 核對 agy 的調查結果，**你自己不核對、不加意見**。不改任何 repo、不 commit、不 push。

1. 先看有沒有既有輸出，執行一次（指令一字不差）：
   \`find ${codexOut(b)} -maxdepth 0 -type f -size +0c\`
   有印出這個路徑＝已存在且非空：直接回報 exit 0、out_ok true、reused true、attempts 0，不跑 codex，到此結束。沒印出（不存在或是空的，指令報錯也算）就往下做。
2. 用 Write 工具把下面的 brief 原文寫進 ${codexBrief(b)}（不要用 heredoc）：
---
${BG}調查目的：${topic}
讀 ${agyOut(b)}（agy 的調查輸出）與它的題目 ${brief(b)}。逐條打開 agy 引用的來源（網址、workflow 檔、文件）核對：每條標「正確／有誤／查不到來源」，有誤就寫出正確內容與來源網址。agy 漏掉的重要事實自己補上，同樣附來源。最後一節「核對後結論」：依核對結果修正後的結論與數量統計。用繁體中文 markdown，不要改任何檔。
---
3. 用 Bash 的 run_in_background 執行（timeout ${BG_TIMEOUT_MS}），指令一字不差：
   \`${run}\`
   **不要用前景執行**：前景 Bash 上限 600 秒，codex 逐條核對大份調查會超過。啟動後等它結束的通知，不要中途放棄、不要另外輪詢或 sleep；結束後讀這個背景指令輸出的那一行 JSON。
4. 重試只限一種情況：JSON 的 ok 是 false，而且 stderr_tail 含 \`at capacity\`（codex 回報模型滿載）。這時重做第 2 步（腳本已刪掉 brief，要重寫），再用 run_in_background（timeout ${BG_TIMEOUT_MS + CAPACITY_WAIT_S * 1000}）執行，指令一字不差：
   \`sleep ${CAPACITY_WAIT_S}; ${run}\`
   同樣等它結束再讀 JSON。最多重試 ${CAPACITY_RETRIES} 次（連第一次共 ${CAPACITY_RETRIES + 1} 次）；逾時（timed_out true）或其他失敗不重試。
5. 依最後一次的 JSON 照實回報：exit＝JSON 的 exit（逾時時 JSON 的 exit 是 null，回報 -1）、out_ok＝JSON 的 ok、reused false、timed_out＝JSON 的 timed_out、attempts＝實際跑 codex_run.py 的次數；ok 是 false 就把 JSON 的 error 與 stderr_tail 寫進 error。不要自己看 shell 的結束碼或輸出檔。`,
      { label: `#${issue} codex:${b.id}`, phase: '核對', schema: CODEX_RUN }).then(c => ({ b, agy: r, codex: c }))
  },
)

const ok = results.filter(x => x && x.codex && x.codex.exit === 0 && x.codex.out_ok)
const failed = results.filter(x => !ok.includes(x)).map(x => ({ id: x?.b?.id, agy: x?.agy, codex: x?.codex }))
if (failed.length) log(`未完成：${failed.map(f => f.id).join('、')}`)
if (!ok.length) return { failed }

phase('整合')
const review = await agent(`你負責整合外部調查的結果。不改任何 repo、不 commit、不 push、不發 issue。

${BG}調查目的：${topic}
資料（每組是 agy 調查與 codex 核對）：
${ok.map(x => `- ${x.b.label}：${agyOut(x.b)}、${codexOut(x.b)}`).join('\n')}

做法：
1. 兩份都讀。codex 標「有誤」或兩者說法不同的地方，自己打開來源抽查（WebFetch），以來源為準。
2. 寫整合結論：每組的主流做法與數量（以核對後的結果為準），各自附代表 repo 與來源連結；組與組之間的差異；對「調查目的」的意涵。
3. agy、codex 與你的判斷不一致、而來源無法判定的，列在「分歧」一節，各方立場都寫，不替任何一方下定論。
4. 沒有來源的主張標明是推論。

用繁體中文 markdown 寫到 ${claudeOut}，回報 output_file 與 summary（結論一節的全文）。`,
  { label: `#${issue} Claude 整合`, phase: '整合', schema: { type: 'object', properties: { output_file: { type: 'string' }, summary: { type: 'string' }, error: { type: 'string' } }, required: ['output_file', 'summary'] } })

if (!post || !review) return { ok: ok.map(x => x.b.id), failed, review }

phase('貼 issue')
// 留言檔的標記、註記行、本機路徑替換與切分由 prepare_comment.py 做並自檢；gh 寫入由子代理逐則下，hook 才看得到
const POST_DIR = `${dir}/post`
// 標題用單引號包，bash 與 fish 都照字面讀；單引號與反斜線先換掉
const q = s => `'${String(s).replace(/'/g, '’').replace(/\\/g, '/')}'`
const items = [
  ...ok.flatMap(x => [
    `--item agy ${agyOut(x.b)} ${q(`${x.b.label} 的 agy 調查原文`)}`,
    `--item codex ${codexOut(x.b)} ${q(`${x.b.label} 的 codex 核對原文`)}`,
  ]),
  `--item claude ${claudeOut} ${q('整合結論')}`,
].join(' ')
const posted = await agent(`把調查結果依序貼到 GitHub issue #${issue}（repo ${REPO}）。不改 repo、不 commit。留言檔由腳本準備，你不要自己加標記、寫註記行、換路徑或切分，也不要改留言檔內容。

1. 執行一次（指令一字不差）：
   \`python3 ${WF}/prepare_comment.py prepare --out-dir ${POST_DIR} --workspace ${WS} ${items}\`
   讀它印出的 JSON。ok 是 false：不貼任何留言，planned 回 0、urls 回空陣列，把 problems 寫進 error，然後停。
2. planned＝JSON 的 files 則數。依 files 的順序，每則用一個獨立的指令貼出（不要用 && 串、不要用迴圈或變數代替路徑、不要在同一個指令裡寫檔）：
   \`gh issue comment ${issue} -R ${REPO} --body-file <files[i].path 的絕對路徑>\`
   記下每則印出的留言網址。某一則失敗（例如被 hook 擋下）就停下，不貼後面的，把原因寫進 error。
3. 最後執行 \`python3 ${WF}/prepare_comment.py clean --out-dir ${POST_DIR}\`（貼失敗也要跑）。

回報 planned（預計則數）、urls（實際貼出的每則網址，依序），有問題寫 error。`,
  { label: `#${issue} 貼 issue`, phase: '貼 issue', schema: { type: 'object', properties: { planned: { type: 'integer' }, urls: { type: 'array', items: { type: 'string' } }, error: { type: 'string' } }, required: ['planned', 'urls'] } })

const urls = posted?.urls ?? []
const planned = posted?.planned ?? 0
let postError = posted?.error ?? ''
if (!posted) postError = '貼 issue 的子代理沒有回傳結果'
else if (planned < 1) postError = postError || '沒有準備出任何留言檔（planned 為 0）'
else if (urls.length !== planned) {
  const diff = planned - urls.length
  const msg = `預計 ${planned} 則，實際貼出 ${urls.length} 則，${diff > 0 ? `少了 ${diff}` : `多了 ${-diff}`} 則`
  log(`貼 issue 不齊：${msg}`)
  postError = postError ? `${msg}；${postError}` : msg
}
const out = { ok: ok.map(x => x.b.id), failed, summary: review.summary, planned, urls }
if (postError) out.error = postError
return out

// args 範例：
// {
//   "issue": 140,
//   "topic": "<一句話說明調查目的>",
//   "background": "<已定案前提>",
//   "briefs": [
//     { "id": "ros", "label": "ROS 生態系" },
//     { "id": "ubuntu", "label": "Canonical／Ubuntu" }
//   ]
// }
