export const meta = {
  name: 'doc-edit',
  description: '改文件：改寫 → lint → 審查 → 潤稿；mode=light 只改寫、審查',
  whenToUse: '改任何現行文件（README、doc/contract/、GLOSSARY.md、ADR）時；主對話不自己改',
  phases: [
    { title: '改寫', detail: '先查 round 是不是 _backup 最大編號加一（不對就停）；每個檔一條並行，由改稿方（預設 codex，editor=claude 時是 Claude 子代理）照 ask 改；codex 改時由包裝子代理驗證備份與有沒有動到範圍外的檔；沒給 ask 就跳過；mode=light 一律由 Claude 子代理改，機械式改動用腳本做並用腳本驗證' },
    { title: 'lint', detail: '全部改完後一個 Claude 子代理跑 check_terms、check_context、check_review_pages、check_messages，只修 lint 指出的地方；mode=light 最後再跑一次當收尾' },
    { title: '審查', detail: '每個檔一條並行，由審查方（改稿方的另一方：預設 Claude，editor=claude 時是 codex）只讀審查；先核對 wayfinder map #78 列的已定案決定；審完的檔立刻進入套用必改；mode=light 一律由另一個 Claude 子代理只看這一輪的 diff 審查' },
    { title: '套用必改', detail: '每個檔由改稿方套用自己的必改，逐條寫已改或未改的理由；建議不改，只回報；mode=light 由 Claude 子代理套用，沒有必改就跳過' },
    { title: '跨檔一致性', detail: 'mode=light 不跑。全部套用完後比對各檔之間的結束碼、編號、名詞、連結；預設 Claude 只讀檢查、清單非空再交 codex 修；editor=claude 時一個 Claude 子代理檢查並修' },
    { title: '潤稿', detail: 'mode=light 不跑。每個檔一個 Claude 子代理並行用 humanizer-zh-tw 潤稿，只准改這一輪改過的行、只修 AI 寫作模式；改完用腳本比對，越界的行還原，這一輪沒改的檔跳過；最後再跑一次 lint' },
  ],
}

// args 契約：
//   repo?        string    預設 '/home/cyc/Desktop/vendor-kit_ws/src'
//   round        string    必填，格式 rNN，必須是 _backup 裡最大的 pre_rNN 加一；備份與審查輸出檔名用
//   topic?       string    短主題（例如 '#121'），跟 round 一起組成這次執行的識別（log 與子代理 label 用）
//   files        string[]  必填，這次只准動的檔（相對 repo 根目錄）
//   ask?         string    要怎麼改；不給就跳過「改寫」
//   background?  string    已定案的前提，改稿方與審查方都不要質疑
//   codex_focus? string    審查額外要看的重點（不論審查方是誰都會附上）
//   editor?      string    'codex'（預設）或 'claude'：誰負責改寫、套用必改、跨檔修正；審查方永遠是另一方
//   mode?        string    'full'（預設）或 'light'
//                          full：改寫 → lint → 審查 → 套用必改 → 跨檔一致性 → 潤稿 → lint，分工照 editor
//                          light：改寫 → lint → 審查 → 套用必改 → lint；全程只用 Claude 子代理（不管 editor，不叫 codex），
//                                 審查只看這一輪的 diff，不跑跨檔一致性與潤稿，目標幾分鐘跑完
//                          何時用 light：機械式改動（換詞、改連結、改編號）、只改幾行、對齊已定案內容的補句；
//                          對外頁的新內容或重寫一律用 full
//   effort?      object    { edit, polish, review }
//                          edit：改稿方的 Claude 子代理（editor=codex 時只作用在包裝 codex 的子代理，不影響 codex 本身）
//                          review：審查方的 Claude 子代理（editor=claude 時只作用在包裝 codex 的子代理）
//                          polish：潤稿子代理（只准改這一輪改過的行，越界的由腳本還原；這一輪沒改的檔跳過）
//                          mode=light 時 edit（含套用必改）與 review 不給就是 'low'；polish 用不到
const {
  repo = '/home/cyc/Desktop/vendor-kit_ws/src',
  round,
  topic = '',
  files,
  ask = '',
  background = '',
  codex_focus = '',
  editor = 'codex',
  mode = 'full',
  effort = {},
} = args ?? {}

// ───────────────── 參數檢查 ─────────────────
if (typeof round !== 'string' || !/^r\d+$/.test(round)) {
  throw new Error('args.round 必填，格式 rNN（例如 "r90"）：備份與審查輸出檔名用的輪次')
}
if (!Array.isArray(files) || files.length === 0 || files.some(f => typeof f !== 'string' || !f.trim())) {
  throw new Error('args.files 必填：至少一個相對 repo 根目錄的檔名，例如 ["README.md"]')
}
if (editor !== 'codex' && editor !== 'claude') {
  throw new Error(`args.editor 只能是 "codex" 或 "claude"（收到 ${JSON.stringify(editor)}）：預設 codex 改、Claude 查`)
}
if (mode !== 'full' && mode !== 'light') {
  throw new Error(`args.mode 只能是 "full" 或 "light"（收到 ${JSON.stringify(mode)}）：預設 full；light 只給機械式或只改幾行的改動`)
}
if (typeof topic !== 'string') {
  throw new Error(`args.topic 只能是字串（收到 ${JSON.stringify(topic)}）：短主題，例如 "#121"`)
}
const LIGHT = mode === 'light'
// 這次執行的識別：meta.name 只能是固定文字，所以每次執行先印出輪次＋主題，子代理 label 也加上輪次（#131）
log(`doc-edit ${round}${topic.trim() ? ` ${topic.trim()}` : ''}${LIGHT ? ' light' : ''}`)
// light 一律 Claude 改、Claude 查（兩個不同的子代理），不叫 codex
const editBy = LIGHT ? 'claude' : editor
const reviewer = LIGHT ? 'claude' : (editor === 'codex' ? 'claude' : 'codex')
const editEffort = effort.edit ?? (LIGHT ? 'low' : undefined)
const reviewEffort = effort.review ?? (LIGHT ? 'low' : undefined)

// 鍵：去掉 .md 或 .csv、/ 換成 _、去掉開頭的點（跟 script/doc/mark_changes.py 同一套）
const key = f => f.replace(/\.(md|csv)$/, '').replace(/\//g, '_').replace(/^\./, '')
// 備份的副檔名：.csv 檔（例如 doc/contract/03_output.csv，#122）備份成 .csv，其他一律 .md
const ext = f => (/\.csv$/.test(f) ? '.csv' : '.md')
// 子代理 label：「<round> 步驟[:檔名]」，檔名只留 basename 去副檔名，例如 r155 改寫:04_interface
const short = f => f.split('/').pop().replace(/\.[^.]+$/, '')
const L = (step, f) => `${round} ${step}${f ? `:${short(f)}` : ''}`
// 這一輪的基準：不帶序號的 <鍵>.pre_<round><副檔名>，一定是這一輪改之前的原檔
const baseOf = f => `${repo}/doc/decisions/_backup/${key(f)}.pre_${round}${ext(f)}`
// 輸出檔依產生者放 review_log/codex/ 或 review_log/claude/
const logFile = (who, name) => `${repo}/doc/decisions/review_log/${who}/${round}-doc-edit-${name}.md`
const BACKGROUND = background.trim()
  ? `背景（已定案，不要質疑、不要重新設計）：\n${background.trim()}`
  : '（沒有額外背景前提。）'
// 已定案的決定記在 GitHub 的 wayfinder map issue #78，每條連到各自的 child issue，結論在 child issue 的留言
const DECIDED = 'wayfinder map issue 的已定案決定（跑 `gh issue view 78 -R ycpss91255-research/vendor_kit --comments`：本文的「Decisions so far」凍結不改，之後的新決定記在留言，兩者都要讀；每條連到一個 child issue；要某條的細節跑 `gh issue view <child> -R ycpss91255-research/vendor_kit --comments`，結論在留言裡；只讀，不要發 issue 或留言）'
// 並行的子代理共用同一個 scratchpad：暫存檔用固定檔名會互相覆蓋（r144 的改前快照與 codex 輸出都被蓋過），
// 所以每個子代理一律放自己的子目錄。label 的檔名只留 basename（不同目錄的同名檔會撞），
// 所以子目錄名取自 tmp（步驟＋完整路徑的鍵），沒給 tmp 才用 label
const tmpDir = name => `<你的 scratchpad>/doc-edit/${round}/${String(name ?? 'agent').replace(/[\/\s:]+/g, '_')}`
const run = (prompt, { tmp, ...opts } = {}) => agent(`${prompt}

暫存檔規則：並行的子代理共用同一個 scratchpad。你的暫存檔（快照、brief、codex 輸出、腳本）一律放 ${tmpDir(tmp ?? opts.label)}/（先 mkdir -p），不要放 scratchpad 根目錄，也不要用別的子代理也可能用的路徑。`, opts)

// ───────────────── 共用護欄（組進每個子代理與 codex 的 prompt） ─────────────────
const guard = scope => `硬性規則（違反就算這輪失敗）：
1. 不 commit、不 push、不跑任何 git 寫入指令（含 add、checkout、reset、stash）。唯讀的 git status／diff 可以。
2. 只准動這幾個檔：
${scope.map(f => `- ${repo}/${f}`).join('\n')}
3. 改前先備份到 ${repo}/doc/decisions/_backup/，命名 <鍵>.pre_${round}<副檔名>。<鍵>：相對 repo 根目錄的路徑，去掉 .md 或 .csv、/ 換成 _、去掉開頭的點（例如 doc/contract/01_purpose.md → doc_contract_01_purpose、.claude/workflows/README.md → claude_workflows_README、doc/contract/03_output.csv → doc_contract_03_output；跟 script/doc/mark_changes.py 同一套）。<副檔名>：.csv 檔是 .csv（doc_contract_03_output.pre_${round}.csv），其他一律 .md。同名已存在就在副檔名前加序號（.pre_${round}.2.md、.pre_${round}.2.csv）；不帶序號的那份一定是這一輪改之前的原檔。
4. 驗證一律用腳本算，不要目視判斷「看起來對」。
5. 名詞照 ${repo}/GLOSSARY.md；_Avoid_ 詞不准出現。對外文件（根 README 與 doc/contract/01～04）裡的名詞，在每頁第一次出現於正文時連到 GLOSSARY.md 該名詞所在分群的標題錨點，不用 <ins>、<u> 或任何 HTML 標籤（規則照 script/doc/check_terms.py）。CSV 檔（doc/contract/*.csv）不准 HTML 與 Markdown，名詞連結不適用；欄位結構（表頭、欄數、引號跳脫、BOM、LF）照 script/doc/check_messages.py。
6. 連結要是有名字的超連結（[名字](路徑)），不要把路徑當連結文字；路徑要實際存在。
7. 同一輪還有別的子代理在並行改這些檔：${files.map(f => f).join('、')}。你只改上面第 2 條列的檔；讀其他檔只為了對照。`
const GUARDRAILS = guard(files)

// check_messages.py 在 doc/contract/03_output.csv 還不存在時自己跳過
const LINT = `cd ${repo} && python3 script/doc/check_terms.py && python3 script/doc/check_context.py && python3 script/doc/check_review_pages.py && python3 script/doc/check_messages.py && python3 script/doc/check_typography.py && python3 script/repo/check_script_layout.py`

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

// codex 指令形狀固定：`< /dev/null` 不可省（省了 codex 會停在等 stdin）；
// 不帶 --sandbox（repo 的 .codex/config.toml 已設 danger-full-access）。
// 外面一律用 bash -c 包起來並印出 codex_exit=：呼叫端的 shell 可能是 fish，
// 用 $status 或 $? 讀結束碼會因 shell 不同拿到空值。
const codexRun = out => `前景執行（Bash timeout 600000，不要 run_in_background），形狀一字不差（<暫存檔> 換成你的暫存檔路徑）：

bash -c 'codex exec --skip-git-repo-check -C ${repo} -o ${out} "$(cat <暫存檔>)" < /dev/null; echo "codex_exit=$?"'

   - \`< /dev/null\` 不可省略，省了 codex 會停在等 stdin。
   - 不要帶 --sandbox：repo 的 .codex/config.toml 已設 danger-full-access。
   - 外層的 \`bash -c '…'\` 與最後的 \`echo "codex_exit=$?"\` 不可省略，也不要另外用 \`$status\` 或 \`$?\` 讀結束碼：結束碼一律從輸出裡 \`codex_exit=\` 那一行抓。
   - 輸出沒有 \`codex_exit=\` 那一行、或值不是 0，就是 codex 失敗：error 寫原因（附 codex_exit 的值與 codex 的錯誤輸出）。`

// ───────────────── 改稿方：依 editor 叫 codex（包裝子代理）或 Claude 子代理；light 一律 Claude ─────────────────
// task 裡已含 guard(scope)；scope 是這一步准動的檔；out 是 codex 輸出檔名（只在 editor=codex 時用）。
// lintMustPass：這一步結束時 lint 必須全部 OK（跨檔修正用）。
const runEditor = ({ label, tmp, ph, task, scope, out, lintMustPass = false }) => {
  const eff = editEffort ? { effort: editEffort } : {}
  if (editBy === 'claude') {
    return run(task, { label, tmp, phase: ph, schema: RESULT, agentType: 'general-purpose', ...eff })
  }
  return run(`你的工作是啟動 codex 改檔，等它結束後自己驗證，再整理成結構化回報。**你自己不改任何檔、不替 codex 補改、不加入你自己的意見。**

硬性規則：不 commit、不 push、不跑任何 git 寫入指令（含 add、checkout、reset、stash）；除了你 scratchpad 裡的暫存檔，不寫任何檔（codex 的輸出檔由 codex 寫）。

這一步 codex 只准動：
${scope.map(f => `- ${repo}/${f}`).join('\n')}
同一輪一起改的檔（其他並行子代理會動它們）：${files.join('、')}

步驟：
1. \`mkdir -p ${repo}/doc/decisions/review_log/codex\`
2. 改前快照，存進 scratchpad：
   - \`git -C ${repo} status --short --untracked-files=all\` 的輸出，以及其中每個路徑的 md5sum，再加上上面准動的每個檔的 md5sum。
   - \`ls ${repo}/doc/decisions/_backup/\` 的輸出。
3. 把下面的 brief 原文用 heredoc（'EOF'）寫進你的 scratchpad 暫存檔。
4. ${codexRun(out)}
5. 驗證（一律用指令算，不要目視）：
   a. 輸出裡沒有 \`codex_exit=\` 那一行、codex_exit 不是 0、或 ${out} 不存在或是空的：error 寫原因（附 codex_exit 的值與 codex 的錯誤輸出）。
   b. 備份：准動的檔裡，md5 跟改前快照不同的，每一個都要在 _backup 多出一份 <鍵>.pre_${round}*<副檔名>（<鍵>：相對 repo 根目錄的路徑去掉 .md 或 .csv、/ 換成 _、去掉開頭的點；<副檔名>：.csv 檔是 .csv，其他是 .md）。少了就寫進 error。
   c. 範圍外：重做一次 git status 與 md5sum 快照，找出新出現或 md5 變了的路徑。不在「同一輪一起改的檔」清單、也不在 doc/decisions/ 底下的，就是 codex 碰到範圍外的檔：列出路徑寫進 error（不要還原，留給主對話處理）。在清單裡但不在這一步准動範圍的變動，是別的並行子代理造成的，不算。
   d. 跑 \`${LINT}\`，輸出原文放進 lint。${lintMustPass ? '有任何 FAIL 就寫進 error。' : '准動的檔造成的 FAIL 寫進 changed 並註明「lint 未過」；別的檔造成的只回報。'}
6. 回報：changed 取自 ${out} 裡 codex 的改動摘要（有「已改／未改：理由」就逐條照原文保留），最後加一行 \`git -C ${repo} diff --stat -- ${scope.join(' ')}\` 的結果；backups 填新增的備份檔路徑。codex 失敗就 error 寫原因，**不要假裝成功**。

brief：
${task}`,
    { label, tmp, phase: ph, schema: RESULT, agentType: 'general-purpose', ...eff })
}

// ───────────────── 輪次檢查 ─────────────────
// round 必須是已用過的最大編號再加一：重用舊編號會蓋掉或混淆那一輪的基準版。
// 已用過的編號有兩個來源：本機 _backup 的 pre_rNN（不進 git，#128），與 git log 的 `Doc-Edit: rNN` footer；
// 換電腦或新 clone 時 _backup 是空的，靠 footer 才不會重用。
// 子代理只負責讀出最大編號，比對在腳本裡做，不交給模型判斷。
const seen = await run(`在 ${repo} 跑這行，照原樣回報輸出的數字（沒有輸出就回 0）；不要做任何其他事：
{ ls doc/decisions/_backup 2>/dev/null | grep -oE 'pre_r[0-9]+' | sed 's/^pre_r//'; git log --format=%B | grep -oE '^Doc-Edit: r[0-9]+' | sed 's/^Doc-Edit: r//'; } | sort -n | tail -1`,
  { label: L('輪次檢查'), phase: '改寫', effort: 'low',
    schema: { type: 'object', properties: { max: { type: 'integer' } }, required: ['max'] } })
const expected = (seen?.max ?? NaN) + 1
if (Number(round.slice(1)) !== expected) {
  throw new Error(`round ${round} 不對：已用過的最大是 r${seen?.max}（_backup 與 git log 的 Doc-Edit footer），這一輪要用 r${expected}；round 不能重用也不能跳號`)
}

// ───────────────── 改寫（每個檔並行） ─────────────────
let edited = null
if (ask.trim()) {
  phase('改寫')
  edited = await parallel(files.map(f => () => runEditor({
    label: L('改寫', f), tmp: `改寫_${key(f)}`, ph: '改寫', scope: [f], out: logFile('codex', `edit-${key(f)}`),
    task: `你負責改文件，這一輪你只負責一個檔：${f}。

${guard([f])}

${BACKGROUND}

這一輪的改動需求（涵蓋多個檔；只做跟 ${f} 有關的部分，其他檔由別的子代理處理）：
${ask.trim()}

步驟：先讀 ${f}，以及它引用的 01、02、GLOSSARY.md 相關段落；照需求改 ${f}；改完跑 \`${LINT}\` 並回報輸出（別的檔造成的 FAIL 只回報，不要修）。不要順手改需求以外的地方。
${LIGHT ? '機械式改動（換詞、改連結、改編號這類）用腳本做（例如 Python re），不要手動逐處改；改完也用腳本驗證（例如 grep 舊說法歸零、新說法的處數對得上）。\n' : ''}最後列出改了哪些地方，一行一條（檔名＋位置＋改了什麼）。`,
  })))
  const bad = edited.map((e, i) => (!e || e.error) ? `${files[i]}：${e?.error ?? '子代理沒有回傳'}` : null).filter(Boolean)
  if (bad.length) {
    log(`改寫失敗：${bad.join('；')}；停在這裡`)
    return { round, mode, edited, linted: null, review: null, applied: null, consistency: null, polished: null, finalLint: null }
  }
}

// ───────────────── lint（全部改完後一次） ─────────────────
phase('lint')
const lintAgent = (label, ph) => run(`你負責讓 lint 歸零。

${GUARDRAILS}

步驟：
1. 跑 \`${LINT}\`。
2. 全部 OK 就直接回報，changed 回空陣列。
3. 有 FAIL：只修 lint 指出的那幾行，而且只在上面列的檔裡修；換詞時照 GLOSSARY.md 的正式名詞。修完重跑，直到全部 OK。
4. lint 指出的問題在列出的檔以外：不要改，寫進 error。`,
  { label, phase: ph, schema: RESULT, agentType: 'general-purpose', effort: 'low' })
const linted = await lintAgent(L('lint'), 'lint')
if (!linted || linted.error) {
  log(`lint 沒有歸零：${linted?.error ?? '子代理沒有回傳'}；停在這裡`)
  return { round, mode, edited, linted, review: null, applied: null, consistency: null, polished: null, finalLint: null }
}

// ───────────────── 審查 → 套用必改（每個檔一條管線） ─────────────────
const briefFor = f => `只讀審查：不要改任何受審的檔。我要的是你的不同意見，不是背書。

${BACKGROUND}

這一輪你只審一個檔：${f}（repo 根目錄 ${repo}）。同一輪一起改的其他檔：${files.filter(x => x !== f).join('、') || '（無）'}；讀它們只為了檢查 ${f} 跟它們一致。

先讀 doc/contract/01_purpose.md、doc/contract/02_invariants.md、GLOSSARY.md、${f} 引用到的 ADR，以及${DECIDED}。

這一輪的改動：用 \`diff -u ${baseOf(f)} ${repo}/${f}\` 看（不帶序號的那份是這一輪改之前的原檔）；這份備份不存在就用 \`git -C ${repo} diff HEAD -- ${f}\`。
${ask.trim() ? `這一輪的改動需求（ask）：\n${ask.trim()}\n` : '這一輪沒有 ask（檔已先改好）。\n'}
請回答（只列 ${f} 裡的問題；跨檔不一致也算在 ${f} 身上，寫明對不上的是哪個檔哪一行）：
0. 已定案（最重要）：逐條對照 map #78 的「Decisions so far」，檢查這一輪的改動有沒有違反任何一條定案；有沒有改變 01 的承諾、削弱 02 的不變量、或改動 03／04 的對外介面而 ask 沒有要求。有就列為必改，fix 寫「還原成…」（附原文），source 寫定案的 child issue（#<child>）或頁名＋行號。
1. 正確性：每一句跟 01、02、GLOSSARY.md、ADR 有沒有對不上的地方？「依 [頁名](連結#錨點) 第 N 條」引用的條號與錨點對不對？對外頁（README、doc/contract/0N）不准有「出處：」行。
2. 連結：每個連結都是有名字的超連結嗎？目標路徑存在嗎？
3. 名詞：有沒有用了 GLOSSARY.md 沒定義的詞、或 _Avoid_ 詞？
4. 易讀性：第一次看的人哪裡看不懂？哪句太長、太繞？
${/0[34]_|README\.md$/.test(f) ? '5. 慣例：涉及使用者介面（結束碼與優先序、選項寫法、說明與用法錯誤、訊息格式）時，逐條對照主流 CLI 慣例（GNU／POSIX、diff、grep、git、Python argparse 等），不一致又沒有理由的列為必改，附慣例來源。' : ''}
${codex_focus.trim() ? `6. 額外重點：${codex_focus.trim()}` : ''}

輸出 markdown，分「必改」「建議」兩區；每條寫位置（檔名＋行號或標題）、問題、建議、證據（檔名＋行號）。不要客套話。`

// light 的審查：只看這一輪的 diff，重點放在有沒有越界，不做全頁的正確性與易讀性審查
const lightBriefFor = f => `只讀審查：不要改任何受審的檔。我要的是你的不同意見，不是背書。你不是改這個檔的那個子代理，不要替改稿方辯護。

${BACKGROUND}

這一輪你只審一個檔：${f}（repo 根目錄 ${repo}）。同一輪一起改的其他檔：${files.filter(x => x !== f).join('、') || '（無）'}。

只看這一輪的改動：\`diff -u ${baseOf(f)} ${repo}/${f}\`（不帶序號的那份是這一輪改之前的原檔）；這份備份不存在就用 \`git -C ${repo} diff HEAD -- ${f}\`。diff 以外的舊內容不審。
${ask.trim() ? `這一輪的改動需求（ask）：\n${ask.trim()}\n` : '這一輪沒有 ask（檔已先改好）。\n'}
對照讀${DECIDED}，需要時再讀 doc/contract/01_purpose.md、doc/contract/02_invariants.md、GLOSSARY.md。只查這幾項（有就列必改，fix 寫「還原成…」或具體改法，source 寫定案的 child issue（#<child>）或檔名＋行號）：
1. 已定案：diff 裡的改動有沒有違反 map #78「Decisions so far」任何一條。
2. 對外承諾：有沒有改變 01 的承諾、削弱 02 的不變量、或改動 03／04 的對外介面，而 ask 沒有要求。
3. 做完沒：ask 要求的每一項在 ${f} 該做的部分都做了嗎？漏的列必改。
4. 連結：diff 裡新增或改動的連結，目標路徑與 #錨點 是不是實際存在（用腳本算 slug 比對，不要目視）。
${codex_focus.trim() ? `5. 額外重點：${codex_focus.trim()}` : ''}
其他看到的問題放「建議」。輸出 markdown，分「必改」「建議」兩區；每條寫位置（檔名＋行號或標題）、問題、建議、證據（檔名＋行號）。不要客套話。`

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

// ───────────────── 審查方：改稿方的另一方 ─────────────────
const runReviewer = f => {
  const out = logFile(reviewer, key(f))
  const eff = reviewEffort ? { effort: reviewEffort } : {}
  if (reviewer === 'claude') {
    return run(`你負責審查一個檔。硬性規則：不 commit、不 push、不跑任何 git 寫入指令；除了下面的審查輸出檔，不改、不建任何檔。

${LIGHT ? lightBriefFor(f) : briefFor(f)}

最後：\`mkdir -p ${repo}/doc/decisions/review_log/claude\`，把上面的 markdown 審查結果寫到 ${out}。回報時「必改」放 must_fix、「建議」放 suggest，每條保留位置、問題、建議、證據（放 source 欄）；output_file 填 ${out}。審不下去（例如檔不存在）就兩個陣列回空、error 寫原因。`,
      { label: L('審查', f), tmp: `審查_${key(f)}`, phase: '審查', schema: REVIEW, agentType: 'general-purpose', ...eff })
  }
  return run(`你的工作是啟動 codex 做只讀審查，再把輸出整理成結構化回報。**不要自己審、不要改檔、不要加入你自己的意見。**

硬性規則：不 commit、不 push、不跑任何 git 寫入指令；不改任何檔。

步驟：
1. \`mkdir -p ${repo}/doc/decisions/review_log/codex\`
2. 把下面的 brief 原文用 heredoc（'EOF'）寫進你的 scratchpad 暫存檔。
3. ${codexRun(out)}
4. 讀 ${out}，「必改」放 must_fix、「建議」放 suggest，每條保留位置、問題、建議、證據（放 source 欄）。output_file 填 ${out}。
5. 輸出裡沒有 \`codex_exit=\` 那一行、codex_exit 不是 0、或 ${out} 不存在或是空的：兩個陣列都回空，error 寫原因（附 codex_exit 的值與 codex 的錯誤輸出）。**不要假裝有結果。**

brief：
${briefFor(f)}`,
    { label: L('審查', f), tmp: `審查_${key(f)}`, phase: '審查', schema: REVIEW, agentType: 'general-purpose', ...eff })
}

const applyOne = (rev, f) => {
  if (!rev || rev.error || !rev.must_fix.length) return Promise.resolve(null)
  return runEditor({
    label: L('套用', f), tmp: `套用_${key(f)}`, ph: '套用必改', scope: [f], out: logFile('codex', `apply-${key(f)}`),
    task: `你負責把審查對 ${f} 的「必改」改進檔裡。建議不要改。

${guard([f])}

${BACKGROUND}

必改清單（JSON）：
${JSON.stringify(rev.must_fix, null, 2)}

規則：
- 每一條都要處理；做法照 fix 欄，但要先對照 source 欄的證據確認審查沒看錯。改法若會削弱 02 的不變量、改變 01 的承諾或 03／04 的對外介面，不要改，註明「未改：改到對外承諾，要維護者決定」。動手前先讀${DECIDED}：改法跟任何一條定案衝突，不要改，註明「未改：跟定案 #<child> 衝突」。確認審查看錯的那條不要改，註明「未改：理由」。
- 必改指到 ${f} 以外的檔：不要改，註明${LIGHT ? '「未改：屬於別的檔，只回報」（這一輪不跑跨檔一致性）' : '「未改：屬於別的檔，交給跨檔一致性」'}。
- 只改必改指到的地方，不要順手改別的。
- 改完跑 \`${LINT}\`；${f} 造成的 FAIL 要修掉，別的檔造成的只回報。
- 最後逐條列出每一條必改的處理結果，一行一條：「已改：位置＋改了什麼」或「未改：理由」（用上面的固定說法）。`,
  })
}

const pairs = await pipeline(files, f => runReviewer(f), (rev, f) => applyOne(rev, f).then(app => ({ f, rev, app })))
const review = {
  reviewer,
  output_files: pairs.map(p => p?.rev?.output_file).filter(Boolean),
  must_fix: pairs.flatMap(p => (p?.rev?.must_fix ?? []).map(x => ({ file: p.f, ...x }))),
  suggest: pairs.flatMap(p => (p?.rev?.suggest ?? []).map(x => ({ file: p.f, ...x }))),
  errors: pairs.filter(p => !p || p.rev?.error || !p.rev).map(p => `${p?.f ?? '?'}：${p?.rev?.error ?? '子代理沒有回傳'}`),
}
const applied = pairs.map(p => p ? { file: p.f, ...(p.app ?? { changed: [], backups: [], lint: '' }) } : null)
const applyErr = applied.filter(a => a && a.error)
if (applyErr.length) {
  log(`套用必改失敗：${applyErr.map(a => `${a.file}：${a.error}`).join('；')}；停在這裡`)
  return { round, mode, edited, linted, review, applied, consistency: null, polished: null, finalLint: null }
}

// ───────────────── light：不跑跨檔一致性與潤稿，最後 lint 收尾 ─────────────────
if (LIGHT) {
  phase('lint')
  const finalLint = await lintAgent(L('最後 lint'), 'lint')
  log(review.errors.length
    ? `light：Claude 審查有失敗：${review.errors.join('；')}`
    : `light：Claude 改、Claude 查：必改 ${review.must_fix.length}（已套用；指到別的檔的只回報）、建議 ${review.suggest.length}（只回報）；沒跑跨檔一致性與潤稿`)
  return { round, mode, edited, linted, review, applied, consistency: null, polished: null, finalLint }
}

// ───────────────── 跨檔一致性（全部套用完後一次） ─────────────────
phase('跨檔一致性')
const otherFile = JSON.stringify(applied.flatMap(a => (a?.changed ?? []).filter(c => /屬於別的檔/.test(c)).map(c => ({ from: a.file, item: c }))), null, 2)
const CHECK_STEPS = `1. 讀這一輪的全部檔。用腳本比對跨檔會一起出現的東西：結束碼與其意思、訊息編號、指令與選項寫法、名詞、互相引用的連結與錨點、同一條規則在兩處的說法。
2. 對不上的地方，照 doc/contract/01～02 與 GLOSSARY.md、${DECIDED}判斷哪邊對、錯的是哪邊；判斷不了的註明「無法判斷，要維護者決定」。
3. 上面那些「屬於別的檔」的必改也要處理。`
let consistency
if (editor === 'claude') {
  // Claude 改稿：一個 Claude 子代理檢查並修
  consistency = await run(`這一輪各檔是分開並行改的，你負責檢查它們之間有沒有對不上，並修掉。

${GUARDRAILS}

${BACKGROUND}

各檔被標為「未改：屬於別的檔」的必改（JSON）：
${otherFile}

步驟：
${CHECK_STEPS}
4. 改錯的那邊；判斷不了的不要改，寫進 changed 並註明「未改：無法判斷，要維護者決定」。
5. 跑 \`${LINT}\`，要全部 OK。`,
    { label: L('跨檔一致性'), phase: '跨檔一致性', schema: RESULT, agentType: 'general-purpose' })
} else {
  // codex 改稿：Claude 只讀檢查出清單，清單非空再交 codex 修
  const CHECK = {
    type: 'object',
    properties: {
      issues: { type: 'array', items: { type: 'object', properties: { file: { type: 'string' }, ...ITEM.properties }, required: ['file', ...ITEM.required] } },
      undecidable: { type: 'array', items: { type: 'string' }, description: '判斷不了哪邊對、要維護者決定的，一行一條' },
      error: { type: 'string', description: '檢查失敗原因；成功留空' },
    },
    required: ['issues', 'undecidable'],
  }
  const check = await run(`這一輪各檔是分開並行改的，你負責只讀檢查它們之間有沒有對不上，列出要修的清單。**不要改任何檔**；不 commit、不 push、不跑任何 git 寫入指令。

這一輪的檔：
${files.map(f => `- ${repo}/${f}`).join('\n')}

${BACKGROUND}

各檔被標為「未改：屬於別的檔」的必改（JSON）：
${otherFile}

步驟：
${CHECK_STEPS}
4. 回報：要修的放 issues（file 是要改的那個檔、where 位置、what 問題、fix 改成什麼、source 證據檔名＋行號）；判斷不了的放 undecidable，不放進 issues。`,
    { label: L('跨檔檢查'), phase: '跨檔一致性', schema: CHECK, agentType: 'general-purpose' })
  if (!check || check.error) {
    consistency = { check, changed: [], backups: [], lint: '', error: check?.error ?? '檢查子代理沒有回傳' }
  } else if (!check.issues.length) {
    consistency = { check, changed: check.undecidable.map(u => `未改：無法判斷，要維護者決定：${u}`), backups: [], lint: '（清單為空，沒有交 codex 修）' }
  } else {
    const fixed = await runEditor({
      label: L('跨檔修正'), ph: '跨檔一致性', scope: files, out: logFile('codex', 'consistency'), lintMustPass: true,
      task: `這一輪各檔是分開並行改的，檢查已找出它們之間對不上的地方，你負責照清單修掉。

${GUARDRAILS}

${BACKGROUND}

要修的清單（JSON）：
${JSON.stringify(check.issues, null, 2)}

規則：
- 每一條先對照 source 欄的證據確認沒看錯；做法照 fix 欄，改 file 欄指的檔。
- 改法跟${DECIDED}任何一條衝突（註明「未改：跟定案 #<child> 衝突」）、或會改變 01 的承諾、削弱 02 的不變量、改動 03／04 的對外介面：不要改，註明「未改：理由」。
- 只改清單指到的地方，不要順手改別的。
- 改完跑 \`${LINT}\`，要全部 OK。
- 最後逐條列出處理結果，一行一條：「已改：檔名＋位置＋改了什麼」或「未改：理由」。`,
    })
    consistency = fixed
      ? { check, ...fixed, changed: [...(fixed.changed ?? []), ...check.undecidable.map(u => `未改：無法判斷，要維護者決定：${u}`)] }
      : { check, changed: [], backups: [], lint: '', error: '跨檔修正子代理沒有回傳' }
  }
}
if (!consistency || consistency.error) {
  log(`跨檔一致性失敗：${consistency?.error ?? '子代理沒有回傳'}；停在這裡`)
  return { round, mode, edited, linted, review, applied, consistency, polished: null, finalLint: null }
}

// ───────────────── 潤稿（每個檔並行） ─────────────────
// 潤稿只准改這一輪改過的行：範圍是「這一輪的基準（不帶序號的 pre_<round> 備份）→ 潤稿前」的新增或修改行。
// 越界檢查用下面的腳本算，不交給模型判斷：比潤稿前與潤稿後，變動落在範圍外的就還原成潤稿前的原文。
// 用法：python3 polish_check.py <基準> <潤稿前> <潤稿後> [--fix]
const POLISH_CHECK = `import sys, difflib, json
base, pre, cur = (open(p, encoding='utf-8').read().splitlines(keepends=True) for p in sys.argv[1:4])
fix = '--fix' in sys.argv[4:]
allowed = set()
for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, base, pre, autojunk=False).get_opcodes():
    if tag in ('replace', 'insert'):
        allowed.update(range(j1, j2))
out, bad = [], []
def keep(i1, i2, j1, j2):
    ok = all(i in allowed for i in range(i1, i2)) if i2 > i1 else (i1 - 1 in allowed or i1 in allowed)
    if ok:
        out.extend(cur[j1:j2])
    else:
        bad.append({'pre_lines': [i1 + 1, i2], 'post_lines': [j1 + 1, j2], 'post_text': ''.join(cur[j1:j2])})
        out.extend(pre[i1:i2])
for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, pre, cur, autojunk=False).get_opcodes():
    if tag == 'equal':
        out.extend(pre[i1:i2])
    elif tag == 'replace' and i2 - i1 == j2 - j1:
        for k in range(i2 - i1):
            keep(i1 + k, i1 + k + 1, j1 + k, j1 + k + 1)
    else:
        keep(i1, i2, j1, j2)
if fix and bad:
    open(sys.argv[3], 'w', encoding='utf-8').write(''.join(out))
print(json.dumps({'round_changed_lines': len(allowed), 'violations': bad, 'reverted': bool(fix and bad)}, ensure_ascii=False))
`
const POLISH_RESULT = {
  type: 'object',
  properties: {
    ...RESULT.properties,
    verify: { type: 'string', description: '越界驗證結果：polish_check.py 兩次輸出的原文（還原前、還原後）；跳過就寫「跳過：這一輪沒有改動」' },
  },
  required: [...RESULT.required, 'verify'],
}
phase('潤稿')
const polished = await parallel(files.map(f => {
  const base = baseOf(f)
  return () => run(`你負責潤稿，只負責 ${f}。

${guard([f])}

${BACKGROUND}

**硬規則：只准改這一輪改過的行。** 違反就算這輪失敗。
- 這一輪的基準是 ${base}（不帶序號的那份就是這一輪改之前的原檔）；它不存在就用 \`git -C ${repo} show HEAD:${f}\` 的輸出（存進 scratchpad）當基準。
- 先跑 \`diff -u <基準> ${repo}/${f}\` 取得這一輪的改動範圍。只在「新增或修改過的行」（diff 裡 + 開頭的行）內潤稿；diff 以外的行一個字都不准動，連標點都不准。
- diff 是空的（這一輪沒改這個檔）：直接跳過，不備份、不呼叫 skill、不改任何東西；changed 與 backups 回空陣列，verify 寫「跳過：這一輪沒有改動」。

步驟：
1. 取得上面的 diff；空的就照上面跳過並回報。
2. 照第 3 條護欄備份 ${f}：不帶序號的那份已經是基準，所以你的備份會帶序號（.pre_${round}.N${ext(f)}，N 取目前最大的加一）。這份是「潤稿前」，記下它的路徑。
3. 用 Skill 工具呼叫 "humanizer-zh-tw"。只修它列出的 AI 寫作模式，而且只在第 1 步的範圍內修；沒有明確對上某個模式就不改。不做同義替換、語序微調、連接詞增刪這類不改善可讀性的改動（例如「所以 VK 要…」不要改成「VK 因此要…」）。
4. 另外：不改意思、不加新事實、不刪承諾或「依 [頁名](連結) 第 N 條」的引用；不動程式碼區塊、行內程式碼、路徑、連結目標、數字、條號、表格結構；CSV 只改欄位裡的文字，不動表頭、逗號、引號與欄數；語氣直接，用「你」或省略主詞，不用「我認為」「建議」「也許」這類軟化詞。這一輪不做文字浮水印檢查，skill 最後的浮水印詢問略過。
5. 跑 \`${LINT}\`；${f} 造成的 FAIL 要修掉，修的時候也只准動第 1 步範圍內的行。
6. 越界驗證（一律用腳本算）：用 Write 工具把下面的腳本原文存成你 scratchpad 的 polish_check.py，然後跑
   \`python3 <scratchpad>/polish_check.py <基準> <潤稿前的備份> ${repo}/${f} --fix\`
   它會找出落在這一輪範圍外的變動，並把那些行還原成潤稿前的原文。有還原（reverted 是 true）就再跑一次同一行指令（不帶 --fix），violations 必須是空的；再跑一次 lint。
7. 回報：changed 列每一處保留下來的改動（原句 → 新句，太長就寫位置與改法，並寫它修的是 humanizer-zh-tw 的哪個模式）；被腳本還原的不算進 changed；verify 放第 6 步每次腳本輸出的原文；backups 放你的備份路徑。

polish_check.py：
${POLISH_CHECK}`,
  { label: L('潤稿', f), tmp: `潤稿_${key(f)}`, phase: '潤稿', schema: POLISH_RESULT, agentType: 'general-purpose', ...(effort.polish ? { effort: effort.polish } : {}) })
}))
const finalLint = await lintAgent(L('最後 lint'), '潤稿')

log(review.errors.length
  ? `${reviewer} 審查有失敗：${review.errors.join('；')}`
  : `${editor} 改、${reviewer} 查：必改 ${review.must_fix.length}（已套用或交跨檔一致性）、建議 ${review.suggest.length}（只回報）`)
return { round, mode, edited, linted, review, applied, consistency, polished, finalLint }

// ───────────────── args 範例（可直接貼進 Workflow 的 args） ─────────────────
// {
//   "round": "r90",
//   "files": ["README.md", "doc/contract/04_interface.md"],
//   "ask": "README 的「專案目的與承諾」改成「目的與承諾」。",
//   "background": "03 是對外契約頁，規則只標 02 的條號、不重述。",
//   "codex_focus": "指令清單的寫法要像 apt、git 的 help：用法一行、指令與說明對齊。",
//   "editor": "codex"
// }
//
// light 範例（機械式或只改幾行的改動）：
// {
//   "round": "r91",
//   "files": ["doc/contract/04_interface.md"],
//   "ask": "04 裡的「訊息 6-3」全部改成「M3」，連結錨點跟著改。",
//   "mode": "light"
// }
