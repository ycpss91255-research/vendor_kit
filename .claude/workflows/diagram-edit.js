export const meta = {
  name: 'diagram-edit',
  description: '改圖：準備 → 改圖（drawio MCP）→ lint 歸零 → 匯出 PNG → codex 審查 → 套用必改 → 收尾檢查；不 commit',
  whenToUse: '改 repo 裡的 .drawio 圖時；主對話已持有 drawio 頁面（reference/drawio_session.txt 有效），workflow 不開新頁',
  phases: [
    { title: '準備', detail: 'script/doc/round.py 取或檢查輪次；script/doc/backup.py save 備份；script/diagram/state.py check 確認頁面有效（失效就停、請維護者在主對話重新取得頁面）；state.py put 把檔載入頁面，並確認要改的頁都在檔裡' },
    { title: '改圖', detail: 'Claude 子代理用 drawio MCP 工具（list_pages、get_diagram、edit_diagram）只改 pages 指定的頁，不呼叫 start_session；改完由 state.py get 存回檔案' },
    { title: 'lint', detail: 'script/diagram/lint.py <file> --base <備份>；指定頁的違規（與 page-id 違規）交回改圖子代理修，最多 3 輪，還不行就停；其他頁的違規只回報' },
    { title: '匯出 PNG', detail: '子代理用 MCP export_diagram 每頁匯出一張到 workspace 的 reference/diagram_review/<round>/，再由 script/diagram/png.py flatten 與 resize 改白底、縮圖' },
    { title: '審查', detail: 'codex 經 script/workflow/codex_run.py 只讀審查 PNG 與 state.py diff，輸出必改與建議' },
    { title: '套用必改', detail: '必改交回改圖子代理（跟改圖同一套做法），存回後重跑 lint 與匯出 PNG；建議只回報給維護者；沒有必改就跳過' },
    { title: '收尾檢查', detail: '再跑一次 lint.py 與 state.py diff：<diagram id> 不准變、不准新增或刪除頁、只有 pages 指定的頁有改動' },
  ],
}

// args 契約：
//   file    string    必填，要改的 .drawio（相對 repo 根目錄，例如 'doc/diagram/architecture.drawio'）
//   pages   string[]  必填，這次只准改的頁的 <diagram id>（圖的持久鍵，不是頁名也不是頁序）
//   task    string    必填，要改什麼
//   round?  string    rNN；不給就用 script/doc/round.py next 取下一個，給了就用 round.py check 檢查（跟 doc-edit 共用編號）
//   repo?       string  預設 '/home/cyc/Desktop/vendor-kit_ws/src'（跟 doc-edit 一樣）
//   workspace?  string  放 PNG 的 workspace，預設 repo 的上一層；repo 是 worktree 時要明確帶主 repo 的上一層
const {
  repo: repoArg = '/home/cyc/Desktop/vendor-kit_ws/src',
  workspace,
  file,
  pages,
  task,
  round: roundArg,
} = args ?? {}

// ───────────────── 參數檢查 ─────────────────
if (typeof repoArg !== 'string' || !repoArg.trim()) {
  throw new Error('args.repo 必須是 repo 的路徑（不給就用預設值）')
}
if (typeof file !== 'string' || !/\.drawio$/.test(file) || file.startsWith('/') || file.split('/').includes('..')) {
  throw new Error('args.file 必填：相對 repo 根目錄的 .drawio 路徑，例如 "doc/diagram/architecture.drawio"（不准絕對路徑、不准 ..）')
}
if (!Array.isArray(pages) || pages.length === 0 || pages.some(p => typeof p !== 'string' || !p.trim())) {
  throw new Error('args.pages 必填：要改的頁的 <diagram id> 陣列，至少一個，例如 ["roles"]')
}
if (new Set(pages).size !== pages.length) {
  throw new Error(`args.pages 有重複的 <diagram id>：${JSON.stringify(pages)}`)
}
if (typeof task !== 'string' || !task.trim()) {
  throw new Error('args.task 必填：要改什麼')
}
if (roundArg !== undefined && (typeof roundArg !== 'string' || !/^r\d+$/.test(roundArg))) {
  throw new Error(`args.round 只能省略或是 rNN（收到 ${JSON.stringify(roundArg)}）；省略就用 script/doc/round.py next 取下一個`)
}

const repo = repoArg.trim().replace(/\/+$/, '')
if (workspace !== undefined && (typeof workspace !== 'string' || !workspace.trim())) {
  throw new Error('args.workspace 只能省略或是路徑：放 PNG 的 workspace（預設 repo 的上一層）')
}
const WS = (workspace ?? repo.replace(/\/[^/]+$/, '')).trim().replace(/\/+$/, '')
const FILE = `${repo}/${file}`
const BASE = file.split('/').pop()
const DOC = `${repo}/script/doc`
const DIA = `${repo}/script/diagram`
const WF = `${repo}/script/workflow`
const MAX_FIX = 3
// 檔名用的頁 id：只留英數、底線、連字號
const safe = s => s.replace(/[^A-Za-z0-9_-]/g, '_')

// 這次執行的識別：meta.name 只能是固定文字，所以開頭印出「diagram-edit <round> <檔名> <頁>」，子代理 label 也帶同一個前綴
let round = roundArg ?? ''
const ID = () => `diagram-edit ${round || '?'} ${BASE} ${pages.join(',')}`
const L = step => `${ID()} ${step}`

// ───────────────── 機械步驟：子代理只跑一行腳本、回報它印出的 JSON ─────────────────
// 判斷成敗在這裡用 JS 做，不交給模型。
const SH = {
  type: 'object',
  properties: { output: { type: 'string', description: '指令在 stdout 印出的最後一行 JSON 原文，一字不改；沒有輸出就留空' } },
  required: ['output'],
}
const sh = async (step, ph, cmd) => {
  const r = await agent(`只跑下面這一行指令（Bash 工具前景執行，timeout 120000），不做任何其他事、不改任何檔、不呼叫任何 MCP 工具：

${cmd}

回報：output 放它在 stdout 印出的最後一行 JSON 原文，一字不改、不摘要、不補欄位。不要另外用 \`$status\` 或 \`$?\` 讀結束碼，成敗看 JSON。`,
    { label: L(step), phase: ph, schema: SH, agentType: 'general-purpose', effort: 'low' })
  try {
    const j = JSON.parse(r?.output ?? '')
    return j && typeof j === 'object' ? j : { ok: false, message: `輸出不是 JSON 物件：${r?.output}` }
  } catch (e) {
    return { ok: false, message: `輸出不是 JSON：${r?.output ?? '（子代理沒有回傳）'}` }
  }
}
const why = j => j?.message ?? j?.error ?? JSON.stringify(j)

// 回傳值：每一步做完就填進去；停下時填 stopped 與 error
const result = {
  round: '', file, pages, backup: '', edits: [], lint: null, png: [], review: null, applied: null, diff: null,
  stopped: null, error: '',
}
const stop = (where, error) => {
  log(`${ID()}：停在「${where}」：${error}`)
  return { ...result, round, stopped: where, error }
}

// ───────────────── 共用護欄（組進每個改圖子代理的 prompt） ─────────────────
const GUARD = `硬性規則（違反就算這輪失敗）：
1. 不 commit、不 push、不跑任何 git 寫入指令（含 add、checkout、reset、stash）。唯讀的 git status／diff 可以。
2. 不准呼叫 drawio MCP 的 start_session：頁面由主對話持有，workflow 只重用（規則見 ${repo}/doc/agents/drawio.md）。也不准呼叫 add_page、delete_page、rename_page、create_new_diagram、load_diagram。
3. 只准改這幾頁（<diagram id>）：${pages.join('、')}。edit_diagram 一律帶 page_id，不用 page_name 或 page_index。其他頁一個 cell 都不准動。
4. 不准改任何頁的 <diagram id>，不准新增、刪除頁或換頁序。
5. 不准用 Write、Edit 或腳本改任何檔；圖只透過 MCP 工具改，存回檔案由 workflow 用 script/diagram/state.py get 做。
6. 樣式照 ${DIA}/STYLE.md；名詞照 ${repo}/GLOSSARY.md（沒有就讀 ${repo}/CONTEXT.md），不用 _Avoid_ 的說法。方塊是最小單位：一格一件事，兩件事就拆成兩格。
7. 驗證用工具算，不要目視判斷「看起來對」。`

const EDIT = {
  type: 'object',
  properties: {
    changed: { type: 'array', items: { type: 'string' }, description: '改了哪些地方，一行一條（頁 id＋cell id＋改了什麼）；套用必改或修 lint 時逐條寫「已改：…」或「未改：理由」' },
    error: { type: 'string', description: '失敗原因；成功留空' },
  },
  required: ['changed'],
}

// 改圖子代理：首次改圖、修 lint、套用必改都用這一個，只換 work 的內容
let editCount = 0
const editDiagram = async (ph, kind, work) => {
  editCount += 1
  const r = await agent(`你負責用 drawio MCP 工具改圖。這一步是：${kind}。

${GUARD}

圖檔：${FILE}（已由 workflow 用 state.py put 載入 drawio 頁面）。
這一輪的改圖需求（task）：
${task.trim()}

步驟：
1. 用 drawio MCP 的 list_pages 確認頁面上的頁 id 包含 ${pages.join('、')}。剛載入時頁面可能還沒更新（實測最多約 72 秒），對不上就再呼叫 list_pages，最多 10 次；還是對不上就停，error 寫「頁面上沒有指定頁」並附 list_pages 的結果。
2. 每個要動的頁先用 get_diagram（帶 page_id）讀目前內容，再用 edit_diagram（帶 page_id）改。edit_diagram 被拒（頁面在瀏覽器裡被改過）就 get_diagram 一次再重試。
3. ${work}
4. 改完再用 get_diagram 讀一次改過的頁，確認改動都在（用工具結果比對，不要目視）。
5. 回報：changed 一行一條。做不到就 error 寫原因，不要假裝成功。`,
    { label: L(`改圖${editCount}`), phase: ph, schema: EDIT, agentType: 'general-purpose' })
  if (!r) return { changed: [], error: '改圖子代理沒有回傳' }
  result.edits.push({ kind, ...r })
  return r
}

// 存回檔案：頁面目前的 XML 寫回 file
const saveBack = async ph => {
  const j = await sh('存回', ph, `python3 ${DIA}/state.py get ${FILE}`)
  return j.ok ? null : `state.py get 失敗：${why(j)}`
}

// ───────────────── lint：指定頁的違規歸零 ─────────────────
// page-id 違規（id 重複、缺或跟備份對不上）一律算在這一輪身上；其他頁的違規不是這一輪造成的，只回報
const runLint = async (ph, step) => {
  const j = await sh(step, ph, `python3 ${DIA}/lint.py ${FILE} --base ${result.backup}`)
  if (!Array.isArray(j.violations)) return { error: `lint.py 沒有正常輸出：${why(j)}` }
  const blocking = j.violations.filter(v => pages.includes(v.page) || v.rule === 'page-id')
  const outside = j.violations.filter(v => !blocking.includes(v))
  return { ok: blocking.length === 0, count: j.count, blocking, outside, skipped: j.skipped ?? [] }
}
const lintToZero = async (ph, tag) => {
  for (let i = 0; ; i++) {
    const lr = await runLint(ph, `${tag}lint${i + 1}`)
    if (lr.error) return lr
    result.lint = lr
    if (lr.ok) return lr
    if (i >= MAX_FIX) return { ...lr, error: `修了 ${MAX_FIX} 輪，指定頁還有 ${lr.blocking.length} 條 lint 違規` }
    const fx = await editDiagram(ph, `修 lint 違規（第 ${i + 1} 輪）`, `只修下面這些 lint 違規（JSON，page 是 <diagram id>、cell 是 cell id、rule 與 msg 是 script/diagram/lint.py 的規則與說明；規則表見 ${DIA}/README.md 的 lint.py 一節），不要順手改別的：
${JSON.stringify(lr.blocking, null, 2)}
違規在不准改的頁、或修它會違反 task：不要改，寫「未改：理由」。`)
    if (fx.error) return { ...lr, error: `修 lint 失敗：${fx.error}` }
    const e = await saveBack(ph)
    if (e) return { ...lr, error: e }
  }
}

// ───────────────── 匯出 PNG：MCP export_diagram 每頁一張，再 png.py 白底＋縮圖 ─────────────────
const PNG_DIR = () => `${WS}/reference/diagram_review/${round}`
const exportPng = async ph => {
  const raw = p => `${PNG_DIR()}/${safe(p)}.raw.png`
  const ex = await agent(`你負責用 drawio MCP 工具匯出 PNG。不改圖、不改任何檔；不准呼叫 start_session、edit_diagram、load_diagram、add_page、delete_page、rename_page。

步驟：
1. \`mkdir -p ${PNG_DIR()}\`。
2. 對每一頁各呼叫一次 drawio MCP 的 export_diagram（format "png"，帶 page_id，path 用下面的絕對路徑）：
${pages.map(p => `   - page_id "${p}" → ${raw(p)}`).join('\n')}
3. 用 \`ls -l\` 確認每個檔都在、大小不是 0。
回報：changed 一行一條（頁 id → 檔案路徑）；有任何一頁匯出失敗，error 寫是哪一頁、工具回了什麼。`,
    { label: L('匯出'), phase: ph, schema: EDIT, agentType: 'general-purpose', effort: 'low' })
  if (!ex || ex.error) return { error: `export_diagram 失敗：${ex?.error ?? '子代理沒有回傳'}` }
  const out = []
  for (const p of pages) {
    const flat = `${PNG_DIR()}/${safe(p)}.flat.png`
    const png = `${PNG_DIR()}/${safe(p)}.png`
    const f = await sh(`白底:${p}`, ph, `python3 ${DIA}/png.py flatten ${raw(p)} ${flat}`)
    if (!f.ok) return { error: `png.py flatten ${p} 失敗：${why(f)}` }
    const r = await sh(`縮圖:${p}`, ph, `python3 ${DIA}/png.py resize ${flat} ${png} --max-width 1600`)
    if (!r.ok) return { error: `png.py resize ${p} 失敗：${why(r)}` }
    out.push(png)
  }
  result.png = out
  return { png: out }
}

// ───────────────── 範圍檢查：state.py diff 備份 → 目前的檔 ─────────────────
const scopeProblems = d => {
  if (!d.ok) return [`state.py diff 失敗：${why(d)}`]
  const p = []
  const ids = xs => (xs ?? []).map(x => x.id ?? x).join('、')
  if (d.pages?.added?.length) p.push(`新增了頁：${ids(d.pages.added)}`)
  if (d.pages?.removed?.length) p.push(`刪除了頁：${ids(d.pages.removed)}`)
  if (d.id_changes?.disappeared?.length || d.id_changes?.appeared?.length) {
    p.push(`<diagram id> 變了：消失 ${ids(d.id_changes.disappeared) || '無'}、新出現 ${ids(d.id_changes.appeared) || '無'}${d.id_changes.same_name?.length ? `（同名換 id：${JSON.stringify(d.id_changes.same_name)}）` : ''}`)
  }
  const renamed = (d.pages?.renamed ?? []).filter(r => !pages.includes(r.id))
  if (renamed.length) p.push(`改了不准改的頁名：${ids(renamed)}`)
  const touched = Object.keys(d.cells ?? {}).filter(id => !pages.includes(id))
  if (touched.length) p.push(`動到不准改的頁：${touched.join('、')}`)
  return p
}
const checkScope = async (ph, step) => {
  const d = await sh(step, ph, `python3 ${DIA}/state.py diff ${result.backup} ${FILE}`)
  const problems = scopeProblems(d)
  result.diff = { changed: d.changed ?? null, pages: d.pages ?? null, cells: d.cells ?? null, id_changes: d.id_changes ?? null, problems }
  return problems
}

// ───────────────── 準備 ─────────────────
phase('準備')
if (round) {
  const j = await sh('輪次', '準備', `python3 ${DOC}/round.py check ${round} --repo ${repo}`)
  if (!j.ok) return stop('準備', `round ${round} 不對：${why(j)}；這一輪要用 ${j.expected ?? j.next ?? '（round.py 沒給）'}，round 不能重用也不能跳號`)
} else {
  const j = await sh('輪次', '準備', `python3 ${DOC}/round.py next --repo ${repo}`)
  if (!j.ok || typeof j.next !== 'string' || !/^r\d+$/.test(j.next)) return stop('準備', `script/doc/round.py next 失敗：${why(j)}`)
  round = j.next
}
result.round = round
log(ID())

// 備份：鍵含副檔名（doc_diagram_architecture.drawio），檔名與序號由 backup.py 算
const bk = await sh('備份', '準備', `python3 ${DOC}/backup.py save --repo ${repo} --round ${round} ${file}`)
const b0 = bk.results?.[0]
if (!bk.ok || !b0 || b0.missing || !b0.backup) {
  return stop('準備', b0?.missing ? `${file} 不存在，沒有東西可備份` : `backup.py save 失敗：${why(bk)}`)
}
result.backup = b0.backup

const ck = await sh('頁面檢查', '準備', `python3 ${DIA}/state.py check`)
if (!ck.ok) {
  return stop('準備', `drawio 頁面失效（${ck.reason ?? '?'}）：${why(ck)}。請維護者在主對話重新取得頁面並更新 workspace 的 reference/drawio_session.txt 後再跑；workflow 不呼叫 start_session`)
}
const put = await sh('載入', '準備', `python3 ${DIA}/state.py put ${FILE}`)
if (!put.ok) return stop('準備', `state.py put 失敗：${why(put)}`)
const have = (put.pages ?? []).map(p => p.id)
const missingPages = pages.filter(p => !have.includes(p))
if (missingPages.length) {
  return stop('準備', `${file} 裡沒有這些 <diagram id>：${missingPages.join('、')}（檔裡有：${have.join('、')}）`)
}

// ───────────────── 改圖 ─────────────────
phase('改圖')
const first = await editDiagram('改圖', '照 task 改圖', `照上面的 task 改 ${pages.join('、')} 這幾頁；不要做 task 以外的改動。`)
if (first.error) return stop('改圖', first.error)
const s1 = await saveBack('改圖')
if (s1) return stop('改圖', s1)

// ───────────────── lint ─────────────────
phase('lint')
const l1 = await lintToZero('lint', '')
if (l1.error) return stop('lint', l1.error)

// ───────────────── 匯出 PNG ─────────────────
phase('匯出 PNG')
const e1 = await exportPng('匯出 PNG')
if (e1.error) return stop('匯出 PNG', e1.error)

// ───────────────── 審查 ─────────────────
phase('審查')
const sc1 = await checkScope('審查', '範圍')
if (sc1.length) return stop('審查', `改到範圍外：${sc1.join('；')}`)

const KEY = file.replace(/\//g, '_').replace(/^\./, '')
const REVIEW_OUT = `${repo}/doc/decisions/review_log/codex/${round}-diagram-edit-${KEY}.md`
const ITEM = {
  type: 'object',
  properties: { where: { type: 'string' }, what: { type: 'string' }, fix: { type: 'string' }, source: { type: 'string' } },
  required: ['where', 'what', 'fix', 'source'],
}
const REVIEW = {
  type: 'object',
  properties: {
    output_file: { type: 'string' },
    must_fix: { type: 'array', items: ITEM },
    suggest: { type: 'array', items: ITEM },
    error: { type: 'string', description: '審查失敗原因；成功留空。失敗時兩個陣列都要是空的，不要編內容' },
  },
  required: ['output_file', 'must_fix', 'suggest'],
}
const brief = `只讀審查一張 drawio 圖這一輪的改動：不要改任何檔，不要呼叫 drawio 服務。我要的是你的不同意見，不是背書。

圖檔：${FILE}；這一輪改之前的備份：${result.backup}。
這一輪只准改的頁（<diagram id>）：${pages.join('、')}。
這一輪的改圖需求（task）：
${task.trim()}

要看的東西：
1. 每頁匯出的 PNG（白底、已縮圖），逐張打開來看：
${result.png.map(p => `   - ${p}`).join('\n')}
2. XML 差異：跑 \`python3 ${DIA}/state.py diff ${result.backup} ${FILE}\`，看它印出的 JSON（每頁以 <diagram id> 對應，列出 cell 的增刪改）；需要細節就直接讀兩份 XML。
3. lint 結果（已歸零的是指定頁；outside 是其他頁本來就有的，只當參考）：
${JSON.stringify(result.lint, null, 2)}
4. 規範：${DIA}/STYLE.md、${repo}/GLOSSARY.md（沒有就讀 ${repo}/CONTEXT.md）、${repo}/doc/decisions/review/01_purpose.md、${repo}/doc/decisions/review/02_invariants.md。

請回答（只列指定頁的問題）：
0. task 要求的每一項都做到了嗎？漏的列必改。
1. 圖上畫的跟 01、02、名詞表有沒有對不上？
2. 看 PNG：有沒有字被截斷、重疊、線穿過方塊、箭頭方向錯、讀不懂的地方？一格是不是只放一件事？
3. 有沒有做了 task 沒要求的改動？有就列必改，fix 寫「還原成…」。
4. 圖例、顏色、樣式有沒有違反 STYLE.md？

輸出 markdown，分「必改」「建議」兩區；每條寫位置（頁 id＋cell id 或圖上的文字）、問題、建議、證據（檔名＋行號、PNG 檔名或 diff 的項目）。不要客套話。`

const rev = await agent(`你的工作是啟動 codex 做只讀審查，再把輸出整理成結構化回報。**不要自己審、不要改檔、不要加入你自己的意見。**

硬性規則：不 commit、不 push、不跑任何 git 寫入指令；除了 brief 暫存檔，不改、不建任何檔；不呼叫任何 MCP 工具。

步驟：
1. 用 Write 工具把下面的 brief 原文寫進你 scratchpad 的 diagram-edit/${round}/review_brief.md（先 mkdir -p）。
2. 前景執行（Bash timeout 600000，不要 run_in_background）：
   python3 ${WF}/codex_run.py --cd ${repo} --brief <brief 檔> --out ${REVIEW_OUT}
   不要自己呼叫 codex，也不要另外用 \`$status\` 或 \`$?\` 讀結束碼：讀腳本印出的一行 JSON。
3. JSON 的 ok 不是 true：兩個陣列都回空，error 寫原因（附 exit、timed_out、error、stderr_tail）。**不要假裝有結果。**
4. ok 是 true：讀 ${REVIEW_OUT}，「必改」放 must_fix、「建議」放 suggest，每條保留位置、問題、建議、證據（放 source 欄）。output_file 填 ${REVIEW_OUT}。

brief：
${brief}`,
  { label: L('審查'), phase: '審查', schema: REVIEW, agentType: 'general-purpose' })
if (!rev || rev.error) return stop('審查', `codex 審查失敗：${rev?.error ?? '子代理沒有回傳'}`)
result.review = rev

// ───────────────── 套用必改 ─────────────────
if (rev.must_fix.length) {
  phase('套用必改')
  const ap = await editDiagram('套用必改', '套用審查的必改', `把下面審查的「必改」改進圖裡；建議不要改：
${JSON.stringify(rev.must_fix, null, 2)}
每一條先對照 source 欄的證據確認審查沒看錯；做法照 fix 欄。改法要動到不准改的頁、跟 task 衝突、或會改變 ${repo}/doc/decisions/review/01_purpose.md 的承諾、削弱 02_invariants.md 的不變量：不要改，寫「未改：理由」。確認審查看錯的那條也不要改，寫「未改：理由」。每一條都要逐條寫「已改：…」或「未改：理由」。`)
  if (ap.error) return stop('套用必改', ap.error)
  result.applied = ap
  const s2 = await saveBack('套用必改')
  if (s2) return stop('套用必改', s2)
  const l2 = await lintToZero('套用必改', '套用後')
  if (l2.error) return stop('套用必改', l2.error)
  const e2 = await exportPng('套用必改')
  if (e2.error) return stop('套用必改', e2.error)
}

// ───────────────── 收尾檢查 ─────────────────
phase('收尾檢查')
const lf = await runLint('收尾檢查', '最後lint')
if (lf.error) return stop('收尾檢查', lf.error)
result.lint = lf
if (!lf.ok) return stop('收尾檢查', `最後 lint 指定頁還有 ${lf.blocking.length} 條違規`)
const scf = await checkScope('收尾檢查', '最後範圍')
if (scf.length) return stop('收尾檢查', `改到範圍外：${scf.join('；')}`)
if (!result.diff.changed) log(`${ID()}：state.py diff 顯示這一輪沒有任何改動`)

log(`${ID()}：改了 ${Object.keys(result.diff.cells ?? {}).join('、') || '（無）'}；lint 指定頁 0 條、其他頁 ${lf.outside.length} 條（只回報）；PNG ${result.png.length} 張；必改 ${rev.must_fix.length}（已交改圖子代理）、建議 ${rev.suggest.length}（只回報）；沒有 commit`)
return { ...result, round }

// ───────────────── args 範例（可直接貼進 Workflow 的 args） ─────────────────
// {
//   "file": "doc/diagram/architecture.drawio",
//   "pages": ["roles"],
//   "task": "角色頁把「維護者」與「使用者」拆成兩格，各自連到 VK；名詞照 GLOSSARY.md。"
// }
//
// 指定輪次、一次改兩頁：
// {
//   "round": "r170",
//   "file": "doc/diagram/architecture.drawio",
//   "pages": ["roles", "flow-init"],
//   "task": "照 #200 的定案重畫這兩頁。"
// }
