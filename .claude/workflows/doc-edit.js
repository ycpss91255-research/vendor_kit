export const meta = {
  name: 'doc-edit',
  description: '改文件的固定流程（每個檔並行）：改寫 → lint 歸零 → 每檔 codex 審查並套用必改 → 跨檔一致性 → 潤稿 → lint；codex 的建議只回報，全程禁止 git 寫入',
  whenToUse: '改任何現行文件（README、docs/contract/、GLOSSARY.md、ADR）時；主對話不自己改',
  phases: [
    { title: '改寫', detail: '先查 round 是不是 _backup 最大編號加一（不對就停）；每個檔一個子代理並行照 ask 改；沒給 ask 就跳過' },
    { title: 'lint', detail: '全部改完後跑一次 check_terms、check_context、check_review_pages，只修 lint 指出的地方' },
    { title: 'codex 審查', detail: '每個檔一個 codex 只讀審查，並行；審完的檔立刻進入套用必改' },
    { title: '套用必改', detail: '每個檔各自套用自己的必改；建議不改，只回報' },
    { title: '跨檔一致性', detail: '全部套用完後，一個子代理比對各檔之間的結束碼、編號、名詞、連結有沒有對不上' },
    { title: '潤稿', detail: '每個檔一個子代理並行用 humanizer-zh-tw 局部潤稿，最後再跑一次 lint' },
  ],
}

// args 契約：
//   repo?        string    預設 '/home/cyc/Desktop/vendor-kit_ws/src'
//   round        string    必填，格式 rNN，必須是 _backup 裡最大的 pre_rNN 加一；備份與 codex 輸出檔名用
//   files        string[]  必填，這次只准動的檔（相對 repo 根目錄）
//   ask?         string    要怎麼改；不給就跳過「改寫」
//   background?  string    已定案的前提，codex 與子代理都不要質疑
//   codex_focus? string    codex 額外要看的重點
//   effort?      object    { edit, polish, review }
const {
  repo = '/home/cyc/Desktop/vendor-kit_ws/src',
  round,
  files,
  ask = '',
  background = '',
  codex_focus = '',
  effort = {},
} = args ?? {}

// ───────────────── 參數檢查 ─────────────────
if (typeof round !== 'string' || !/^r\d+$/.test(round)) {
  throw new Error('args.round 必填，格式 rNN（例如 "r90"）：備份與 codex 輸出檔名用的輪次')
}
if (!Array.isArray(files) || files.length === 0 || files.some(f => typeof f !== 'string' || !f.trim())) {
  throw new Error('args.files 必填：至少一個相對 repo 根目錄的檔名，例如 ["README.md"]')
}

const key = f => f.replace(/\.md$/, '').replace(/\//g, '_').replace(/^\./, '')
const codexOut = f => `${repo}/doc/decisions/review_log/codex/${round}-doc-edit-${key(f)}.md`
const BACKGROUND = background.trim()
  ? `背景（已定案，不要質疑、不要重新設計）：\n${background.trim()}`
  : '（沒有額外背景前提。）'

// ───────────────── 共用護欄（組進每個子代理的 prompt） ─────────────────
const guard = scope => `硬性規則（違反就算這輪失敗）：
1. 不 commit、不 push、不跑任何 git 寫入指令（含 add、checkout、reset、stash）。唯讀的 git status／diff 可以。
2. 只准動這幾個檔：
${scope.map(f => `- ${repo}/${f}`).join('\n')}
3. 改前先備份到 ${repo}/doc/decisions/_backup/，命名 <鍵>.pre_${round}.md。<鍵>：相對 repo 根目錄的路徑，去掉 .md、/ 換成 _、去掉開頭的點（例如 .claude/workflows/README.md → claude_workflows_README；跟 script/mark_changes.py 同一套）。同名已存在就在 .md 前加序號（.pre_${round}.2.md）；不帶序號的那份一定是這一輪改之前的原檔。
4. 驗證一律用腳本算，不要目視判斷「看起來對」。
5. 名詞照 ${repo}/GLOSSARY.md；_Avoid_ 詞不准出現。名詞底線用 <ins>，不用 <u>（GitHub 會刪掉 <u>）。
6. 連結要是有名字的超連結（[名字](路徑)），不要把路徑當連結文字；路徑要實際存在。
7. 同一輪還有別的子代理在並行改這些檔：${files.map(f => f).join('、')}。你只改上面第 2 條列的檔；讀其他檔只為了對照。`
const GUARDRAILS = guard(files)

const LINT = `cd ${repo} && python3 script/check_terms.py && python3 script/check_context.py && python3 script/check_review_pages.py`

const RESULT = {
  type: 'object',
  properties: {
    changed: { type: 'array', items: { type: 'string' }, description: '改了哪些地方，一行一條（檔名＋位置＋改了什麼）' },
    backups: { type: 'array', items: { type: 'string' }, description: '備份檔路徑' },
    lint: { type: 'string', description: '最後一次 lint 的輸出（原文）' },
    error: { type: 'string', description: '失敗原因；成功留空' },
  },
  required: ['changed', 'backups', 'lint'],
}

// ───────────────── 輪次檢查 ─────────────────
// round 必須是 _backup 裡最大的 pre_rNN 再加一：重用舊編號會蓋掉或混淆那一輪的基準版。
// 子代理只負責讀出最大編號，比對在腳本裡做，不交給模型判斷。
const seen = await agent(`在 ${repo} 跑這行，照原樣回報輸出的數字（沒有輸出就回 0）；不要做任何其他事：
ls doc/decisions/_backup | grep -oE 'pre_r[0-9]+' | sed 's/^pre_r//' | sort -n | tail -1`,
  { label: '輪次檢查', phase: '改寫', effort: 'low',
    schema: { type: 'object', properties: { max: { type: 'integer' } }, required: ['max'] } })
const expected = (seen?.max ?? NaN) + 1
if (Number(round.slice(1)) !== expected) {
  throw new Error(`round ${round} 不對：_backup 裡最大是 pre_r${seen?.max}，這一輪要用 r${expected}；round 不能重用也不能跳號`)
}

// ───────────────── 改寫（每個檔並行） ─────────────────
let edited = null
if (ask.trim()) {
  phase('改寫')
  edited = await parallel(files.map(f => () => agent(`你負責改文件，這一輪你只負責一個檔：${f}。

${guard([f])}

${BACKGROUND}

這一輪的改動需求（涵蓋多個檔；只做跟 ${f} 有關的部分，其他檔由別的子代理處理）：
${ask.trim()}

步驟：先讀 ${f}，以及它引用的 01、02、GLOSSARY.md 相關段落；照需求改 ${f}；改完跑 \`${LINT}\` 並回報輸出（別的檔造成的 FAIL 只回報，不要修）。不要順手改需求以外的地方。`,
    { label: `改寫:${f}`, phase: '改寫', schema: RESULT, agentType: 'general-purpose', ...(effort.edit ? { effort: effort.edit } : {}) })))
  const bad = edited.map((e, i) => (!e || e.error) ? `${files[i]}：${e?.error ?? '子代理沒有回傳'}` : null).filter(Boolean)
  if (bad.length) {
    log(`改寫失敗：${bad.join('；')}；停在這裡`)
    return { round, edited, linted: null, review: null, applied: null, consistency: null, polished: null }
  }
}

// ───────────────── lint（全部改完後一次） ─────────────────
phase('lint')
const lintAgent = (label, ph) => agent(`你負責讓 lint 歸零。

${GUARDRAILS}

步驟：
1. 跑 \`${LINT}\`。
2. 全部 OK 就直接回報，changed 回空陣列。
3. 有 FAIL：只修 lint 指出的那幾行，而且只在上面列的檔裡修；換詞時照 GLOSSARY.md 的正式名詞。修完重跑，直到全部 OK。
4. lint 指出的問題在列出的檔以外：不要改，寫進 error。`,
  { label, phase: ph, schema: RESULT, agentType: 'general-purpose', effort: 'low' })
const linted = await lintAgent('lint', 'lint')
if (!linted || linted.error) {
  log(`lint 沒有歸零：${linted?.error ?? '子代理沒有回傳'}；停在這裡`)
  return { round, edited, linted, review: null, applied: null, consistency: null, polished: null }
}

// ───────────────── codex 審查 → 套用必改（每個檔一條管線） ─────────────────
const briefFor = f => `只讀，不要改任何檔。我要的是你的不同意見，不是背書。

${BACKGROUND}

這一輪你只審一個檔：${f}（repo 根目錄 ${repo}）。同一輪一起改的其他檔：${files.filter(x => x !== f).join('、') || '（無）'}；讀它們只為了檢查 ${f} 跟它們一致。

先讀 docs/contract/01_purpose.md、docs/contract/02_invariants.md、GLOSSARY.md，以及 ${f} 引用到的 ADR。

請回答（只列 ${f} 裡的問題；跨檔不一致也算在 ${f} 身上，寫明對不上的是哪個檔哪一行）：
1. 正確性：每一句跟 01、02、GLOSSARY.md、ADR 有沒有對不上的地方？「依 [頁名](連結#錨點) 第 N 條」引用的條號與錨點對不對？對外頁（README、docs/contract/0N）不准有「出處：」行。
2. 連結：每個連結都是有名字的超連結嗎？目標路徑存在嗎？
3. 名詞：有沒有用了 GLOSSARY.md 沒定義的詞、或 _Avoid_ 詞？
4. 易讀性：第一次看的人哪裡看不懂？哪句太長、太繞？
${/0[34]_|README\.md$/.test(f) ? '5. 慣例：涉及使用者介面（結束碼與優先序、選項寫法、說明與用法錯誤、訊息格式）時，逐條對照主流 CLI 慣例（GNU／POSIX、diff、grep、git、Python argparse 等），不一致又沒有理由的列為必改，附慣例來源。' : ''}
${codex_focus.trim() ? `6. 額外重點：${codex_focus.trim()}` : ''}

輸出 markdown，分「必改」「建議」兩區；每條寫位置（檔名＋行號或標題）、問題、建議、證據（檔名＋行號）。不要客套話。`

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
    error: { type: 'string', description: 'codex 失敗原因；成功留空。失敗時兩個陣列都要是空的，不要編內容' },
  },
  required: ['output_file', 'must_fix', 'suggest'],
}

const reviewOne = f => agent(`你的工作是啟動 codex 做只讀審查，再把輸出整理成結構化回報。**不要自己審、不要改檔、不要加入你自己的意見。**

硬性規則：不 commit、不 push、不跑任何 git 寫入指令；不改任何檔。

步驟：
1. \`mkdir -p ${repo}/doc/decisions/review_log/codex\`
2. 把下面的 brief 原文用 heredoc（'EOF'）寫進你的 scratchpad 暫存檔。
3. 前景執行（Bash timeout 600000，不要 run_in_background），形狀一字不差：

codex exec --skip-git-repo-check -C ${repo} -o ${codexOut(f)} "$(cat <暫存檔>)" < /dev/null

   - \`< /dev/null\` 不可省略，省了 codex 會停在等 stdin。
   - 不要帶 --sandbox：repo 的 .codex/config.toml 已設 danger-full-access。
4. 讀 ${codexOut(f)}，「必改」放 must_fix、「建議」放 suggest，每條保留位置、問題、建議、證據（放 source 欄）。output_file 填 ${codexOut(f)}。
5. codex 失敗或輸出是空的：兩個陣列都回空，error 寫原因。**不要假裝有結果。**

brief：
${briefFor(f)}`,
  { label: `codex:${f}`, phase: 'codex 審查', schema: REVIEW, agentType: 'general-purpose', ...(effort.review ? { effort: effort.review } : {}) })

const applyOne = (rev, f) => {
  if (!rev || rev.error || !rev.must_fix.length) return Promise.resolve(null)
  return agent(`你負責把 codex 對 ${f} 的「必改」改進檔裡。建議不要改。

${guard([f])}

${BACKGROUND}

必改清單（JSON）：
${JSON.stringify(rev.must_fix, null, 2)}

規則：
- 每一條都要處理；做法照 fix 欄，但要先對照 source 欄的證據確認 codex 沒看錯。改法若會削弱 02 的不變量、改變 01 的承諾或 03／04 的對外介面，不要改，寫進 changed 並註明「未改：改到對外承諾，要維護者決定」。動手前先讀 ${repo}/doc/decisions/review_log/discussion_queue.md 的「已定案」區：改法跟任何一條定案衝突，不要改，寫進 changed 並註明「未改：跟定案第 N 條衝突」。確認 codex 看錯的那條不要改，寫進 changed 並註明「未改：理由」。
- 必改指到 ${f} 以外的檔：不要改，寫進 changed 並註明「未改：屬於別的檔，交給跨檔一致性」。
- 只改必改指到的地方，不要順手改別的。
- 改完跑 \`${LINT}\`；${f} 造成的 FAIL 要修掉，別的檔造成的只回報。`,
    { label: `套用:${f}`, phase: '套用必改', schema: RESULT, agentType: 'general-purpose', ...(effort.edit ? { effort: effort.edit } : {}) })
}

const pairs = await pipeline(files, f => reviewOne(f), (rev, f) => applyOne(rev, f).then(app => ({ f, rev, app })))
const review = {
  output_files: pairs.map(p => p?.rev?.output_file).filter(Boolean),
  must_fix: pairs.flatMap(p => (p?.rev?.must_fix ?? []).map(x => ({ file: p.f, ...x }))),
  suggest: pairs.flatMap(p => (p?.rev?.suggest ?? []).map(x => ({ file: p.f, ...x }))),
  errors: pairs.filter(p => !p || p.rev?.error || !p.rev).map(p => `${p?.f ?? '?'}：${p?.rev?.error ?? '子代理沒有回傳'}`),
}
const applied = pairs.map(p => p ? { file: p.f, ...(p.app ?? { changed: [], backups: [], lint: '' }) } : null)
const applyErr = applied.filter(a => a && a.error)
if (applyErr.length) {
  log(`套用必改失敗：${applyErr.map(a => `${a.file}：${a.error}`).join('；')}；停在這裡`)
  return { round, edited, linted, review, applied, consistency: null, polished: null }
}

// ───────────────── 跨檔一致性（全部套用完後一次） ─────────────────
phase('跨檔一致性')
const consistency = await agent(`這一輪各檔是分開並行改的，你負責檢查它們之間有沒有對不上，並修掉。

${GUARDRAILS}

${BACKGROUND}

各檔被標為「未改：屬於別的檔」的必改（JSON）：
${JSON.stringify(applied.flatMap(a => (a?.changed ?? []).filter(c => /屬於別的檔/.test(c)).map(c => ({ from: a.file, item: c }))), null, 2)}

步驟：
1. 讀這一輪的全部檔。用腳本比對跨檔會一起出現的東西：結束碼與其意思、訊息編號、指令與選項寫法、名詞、互相引用的連結與錨點、同一條規則在兩處的說法。
2. 對不上的地方，照 docs/contract/01～02 與 GLOSSARY.md、discussion_queue.md 已定案區判斷哪邊對，改錯的那邊；判斷不了的不要改，寫進 changed 並註明「未改：無法判斷，要維護者決定」。
3. 處理上面那些「屬於別的檔」的必改。
4. 跑 \`${LINT}\`，要全部 OK。`,
  { label: '跨檔一致性', phase: '跨檔一致性', schema: RESULT, agentType: 'general-purpose' })
if (!consistency || consistency.error) {
  log(`跨檔一致性失敗：${consistency?.error ?? '子代理沒有回傳'}；停在這裡`)
  return { round, edited, linted, review, applied, consistency, polished: null }
}

// ───────────────── 潤稿（每個檔並行） ─────────────────
phase('潤稿')
const polished = await parallel(files.map(f => () => agent(`你負責潤稿，只負責 ${f}。先用 Skill 工具呼叫 "humanizer-zh-tw"，照它的規則對 ${f} 做**局部**潤稿。

${guard([f])}

${BACKGROUND}

額外規則：
- 不改意思、不加新事實、不刪承諾或「依 [頁名](連結) 第 N 條」的引用。
- 不動程式碼區塊、行內程式碼、路徑、連結目標、數字、條號、表格結構。
- 語氣直接，用「你」或省略主詞；不用「我認為」「建議」「也許」這類軟化詞。
- 這一輪不做文字浮水印檢查，skill 最後的浮水印詢問略過。
- 改完跑 \`${LINT}\`；${f} 造成的 FAIL 要修掉。

回報每一處改動（原句 → 新句，太長就寫位置與改法）。`,
  { label: `潤稿:${f}`, phase: '潤稿', schema: RESULT, agentType: 'general-purpose', ...(effort.polish ? { effort: effort.polish } : {}) })))
const finalLint = await lintAgent('最後 lint', '潤稿')

log(review.errors.length
  ? `codex 審查有失敗：${review.errors.join('；')}`
  : `codex：必改 ${review.must_fix.length}（已套用或交跨檔一致性）、建議 ${review.suggest.length}（只回報）`)
return { round, edited, linted, review, applied, consistency, polished, finalLint }

// ───────────────── args 範例（可直接貼進 Workflow 的 args） ─────────────────
// {
//   "round": "r90",
//   "files": ["README.md", "docs/contract/04_interface.md"],
//   "ask": "README 的「專案目的與承諾」改成「目的與承諾」。",
//   "background": "03 是對外契約頁，規則只標 02 的條號、不重述。",
//   "codex_focus": "指令清單的寫法要像 apt、git 的 help：用法一行、指令與說明對齊。"
// }
