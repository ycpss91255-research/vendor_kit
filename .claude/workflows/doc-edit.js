export const meta = {
  name: 'doc-edit',
  description: '改文件的固定流程：改寫 → lint 歸零 → codex 只讀審查 → 套用必改 → humanizer-zh-tw 潤稿；codex 的建議只回報，全程禁止 git 寫入',
  whenToUse: '改任何現行文件（README、doc/decisions/review/、CONTEXT.md、ADR）時；主對話不自己改',
  phases: [
    { title: '改寫', detail: '一個子代理照 ask 改指定檔；沒給 ask 就跳過（檔已經改好，只跑後面三段）' },
    { title: 'lint', detail: '跑 check_terms 與 check_context，只修 lint 指出的地方，直到全部通過' },
    { title: 'codex 審查', detail: '子代理啟動 codex 只讀審查，對照 01、02、CONTEXT.md、ADR，整理成必改／建議' },
    { title: '套用必改', detail: 'codex 的必改直接改進檔裡並跑 lint；建議不改，只回報給維護者' },
    { title: '潤稿', detail: '子代理用 humanizer-zh-tw 做局部潤稿，不改意思、不動程式碼與連結，改完再跑一次 lint' },
  ],
}

// args 契約：
//   repo?        string    預設 '/home/cyc/Desktop/vendor-kit_ws/src'
//   round        string    必填，備份與 codex 輸出檔名用，例如 'r90'
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
if (typeof round !== 'string' || !round.trim()) {
  throw new Error('args.round 必填：備份與 codex 輸出檔名用的輪次字串，例如 "r90"')
}
if (!Array.isArray(files) || files.length === 0 || files.some(f => typeof f !== 'string' || !f.trim())) {
  throw new Error('args.files 必填：至少一個相對 repo 根目錄的檔名，例如 ["README.md"]')
}

const FILES = files.map(f => `- ${repo}/${f}`).join('\n')
const CODEX_OUT = `${repo}/doc/decisions/review_log/codex/${round}-doc-edit.md`
const BACKGROUND = background.trim()
  ? `背景（已定案，不要質疑、不要重新設計）：\n${background.trim()}`
  : '（沒有額外背景前提。）'

// ───────────────── 共用護欄（組進每個子代理的 prompt） ─────────────────
const GUARDRAILS = `硬性規則（違反就算這輪失敗）：
1. 不 commit、不 push、不跑任何 git 寫入指令（含 add、checkout、reset、stash）。唯讀的 git status／diff 可以。
2. 只准動這幾個檔：
${FILES}
3. 改前先備份到 ${repo}/doc/decisions/_backup/，命名 <鍵>.pre_${round}.md。<鍵>：相對 repo 根目錄的路徑，去掉 .md、/ 換成 _、去掉開頭的點（例如 .claude/workflows/README.md → claude_workflows_README；跟 script/mark_changes.py 同一套）。同名已存在就在 .md 前加序號（.pre_${round}.2.md）；不帶序號的那份一定是這一輪改之前的原檔。
4. 驗證一律用腳本算，不要目視判斷「看起來對」。
5. 名詞照 ${repo}/CONTEXT.md；_Avoid_ 詞不准出現。名詞底線用 <ins>，不用 <u>（GitHub 會刪掉 <u>）。
6. 連結要是有名字的超連結（[名字](路徑)），不要把路徑當連結文字；路徑要實際存在。`

const LINT = `cd ${repo} && python3 script/check_terms.py && python3 script/check_context.py`

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

// ───────────────── 改寫 ─────────────────
let edited = null
if (ask.trim()) {
  phase('改寫')
  edited = await agent(`你負責改文件。

${GUARDRAILS}

${BACKGROUND}

要做的改動：
${ask.trim()}

步驟：先讀完要改的檔，以及它們引用的 01、02、CONTEXT.md 相關段落；照改動需求改；改完跑 \`${LINT}\` 並回報輸出。不要順手改需求以外的地方。`,
    { label: '改寫', phase: '改寫', schema: RESULT, agentType: 'general-purpose', ...(effort.edit ? { effort: effort.edit } : {}) })
  if (!edited || edited.error) {
    log(`改寫失敗：${edited?.error ?? '子代理沒有回傳'}；停在這裡`)
    return { round, edited, linted: null, polished: null, review: null }
  }
}

// ───────────────── lint ─────────────────
phase('lint')
const linted = await agent(`你負責讓 lint 歸零。

${GUARDRAILS}

步驟：
1. 跑 \`${LINT}\`。
2. 全部 OK 就直接回報，changed 回空陣列。
3. 有 FAIL：只修 lint 指出的那幾行，而且只在上面列的檔裡修；換詞時照 CONTEXT.md 的正式名詞。修完重跑，直到全部 OK。
4. lint 指出的問題在列出的檔以外：不要改，寫進 error。`,
  { label: 'lint', phase: 'lint', schema: RESULT, agentType: 'general-purpose', effort: 'low' })
if (!linted || linted.error) {
  log(`lint 沒有歸零：${linted?.error ?? '子代理沒有回傳'}；停在這裡`)
  return { round, edited, linted, polished: null, review: null }
}

// ───────────────── codex 審查 ─────────────────
const brief = `只讀，不要改任何檔。我要的是你的不同意見，不是背書。

${BACKGROUND}

審這幾個檔（repo 根目錄 ${repo}）：
${files.map(f => `- ${f}`).join('\n')}

先讀 doc/decisions/review/01_purpose.md、doc/decisions/review/02_invariants.md、CONTEXT.md，以及檔中引用到的 ADR。

請回答：
1. 正確性：每一句跟 01、02、CONTEXT.md、ADR 有沒有對不上的地方？出處標的條號、章節對不對？
2. 連結：每個連結都是有名字的超連結嗎？目標路徑存在嗎？
3. 名詞：有沒有用了 CONTEXT.md 沒定義的詞、或 _Avoid_ 詞？
4. 易讀性：第一次看的人哪裡看不懂？哪句太長、太繞？
${codex_focus.trim() ? `5. 額外重點：${codex_focus.trim()}` : ''}

輸出 markdown，分「必改」「建議」兩區；每條寫位置（檔名＋行號或標題）、問題、建議、出處。不要客套話。`

const ITEM = {
  type: 'object',
  properties: {
    where: { type: 'string' },
    what: { type: 'string' },
    fix: { type: 'string' },
    source: { type: 'string' },
  },
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

phase('codex 審查')
const review = await agent(`你的工作是啟動 codex 做只讀審查，再把輸出整理成結構化回報。**不要自己審、不要改檔、不要加入你自己的意見。**

${GUARDRAILS.split('\n').slice(0, 2).join('\n')}

步驟：
1. \`mkdir -p ${repo}/doc/decisions/review_log/codex\`
2. 把下面的 brief 原文用 heredoc（'EOF'）寫進你的 scratchpad 暫存檔。
3. 前景執行（Bash timeout 600000，不要 run_in_background），形狀一字不差：

codex exec --skip-git-repo-check -C ${repo} -o ${CODEX_OUT} "$(cat <暫存檔>)" < /dev/null

   - \`< /dev/null\` 不可省略，省了 codex 會停在等 stdin。
   - 不要帶 --sandbox：repo 的 .codex/config.toml 已設 danger-full-access。
4. 讀 ${CODEX_OUT}，「必改」放 must_fix、「建議」放 suggest，每條保留位置、問題、建議、出處。output_file 填 ${CODEX_OUT}。
5. codex 失敗或輸出是空的：兩個陣列都回空，error 寫原因。**不要假裝有結果。**

brief：
${brief}`,
  { label: 'codex 審查', phase: 'codex 審查', schema: REVIEW, agentType: 'general-purpose', ...(effort.review ? { effort: effort.review } : {}) })

// ───────────────── 套用必改 ─────────────────
// 必改一律直接套用，不問維護者；建議才回報。
let applied = null
if (review && !review.error && review.must_fix.length) {
  phase('套用必改')
  applied = await agent(`你負責把 codex 的「必改」全部改進檔裡。建議不要改。

${GUARDRAILS}

${BACKGROUND}

必改清單（JSON）：
${JSON.stringify(review.must_fix, null, 2)}

規則：
- 每一條都要處理；做法照 fix 欄，但要先對照 source 欄的出處確認 codex 沒看錯。確認 codex 看錯的那條不要改，寫進 changed 並註明「未改：理由」。
- 只改必改指到的地方，不要順手改別的。
- 改完跑 \`${LINT}\`，要全部 OK。`,
    { label: '套用必改', phase: '套用必改', schema: RESULT, agentType: 'general-purpose', ...(effort.edit ? { effort: effort.edit } : {}) })
  if (!applied || applied.error) {
    log(`套用必改失敗：${applied?.error ?? '子代理沒有回傳'}；停在這裡`)
    return { round, edited, linted, review, applied, polished: null }
  }
}

// ───────────────── 潤稿 ─────────────────
phase('潤稿')
const polished = await agent(`你負責潤稿。先用 Skill 工具呼叫 "humanizer-zh-tw"，照它的規則對下面的檔做**局部**潤稿。

${GUARDRAILS}

${BACKGROUND}

額外規則：
- 不改意思、不加新事實、不刪承諾或出處。
- 不動程式碼區塊、行內程式碼、路徑、連結目標、數字、條號、表格結構。
- 語氣直接，用「你」或省略主詞；不用「我認為」「建議」「也許」這類軟化詞。
- 這一輪不做文字浮水印檢查，skill 最後的浮水印詢問略過。
- 改完跑 \`${LINT}\`，要全部 OK；不 OK 就把你造成的問題修掉。

回報每一處改動（原句 → 新句，太長就寫位置與改法）。`,
  { label: '潤稿', phase: '潤稿', schema: RESULT, agentType: 'general-purpose', ...(effort.polish ? { effort: effort.polish } : {}) })
if (!polished || polished.error) {
  log(`潤稿失敗：${polished?.error ?? '子代理沒有回傳'}；停在這裡`)
  return { round, edited, linted, review, applied, polished }
}


log(review && !review.error
  ? `codex：必改 ${review.must_fix.length}（已套用）、建議 ${review.suggest.length}（只回報）`
  : `codex 審查失敗：${review?.error ?? '子代理沒有回傳'}`)
return { round, edited, linted, review, applied, polished }

// ───────────────── args 範例（可直接貼進 Workflow 的 args） ─────────────────
// {
//   "round": "r90",
//   "files": ["README.md", "doc/decisions/review/03_interface.md"],
//   "ask": "README 的「專案目的與承諾」改成「目的與承諾」。",
//   "background": "03 是對外契約頁，規則只標 02 的條號、不重述。",
//   "codex_focus": "指令清單的寫法要像 apt、git 的 help：用法一行、指令與說明對齊。"
// }
