export const meta = {
  name: 'discuss',
  description: 'codex 與 Claude 各自回答、最多 3 輪比對，未收斂交維護者',
  whenToUse: '問維護者之前；結果回報主對話，貼到 #78 對應的 child issue',
  phases: [
    { title: '準備', detail: '不論有沒有給 repo，派一個 effort low 子代理在 repo（沒給就用工作目錄）跑 git rev-parse --git-common-dir 查出主 repo；腳本一律從主 repo 取，repo 只決定 codex 讀哪份檔與輸出位置' },
    { title: '內部對照', detail: '必跑：一個 Claude 子代理在 repo 讀已定案資料（01–04、reason_codes.csv、GLOSSARY.md 或 CONTEXT.md、全部 ADR、scope_roadmap.md）、args.issues 指定的 issue 與依關鍵字搜到的相關 issue；每題回報已定依據（檔名:行號或 issue 留言）、能否只靠既有規則推出答案、題目前提與定案的衝突。不存在的檔記下來，不失敗' },
    { title: '各自回答', detail: '第 1 輪：每題 codex（只讀）與 Claude 子代理各答一次，互不知道對方的答案；內部對照結果是不可質疑的前提，回答必須先引用內部依據（internal_basis 不得為空，空的重試一次，仍空就記錯）' },
    { title: '回應', detail: '第 2、3 輪：上一輪不一致的題，把對方最新立場交給雙方各自回應，證據成立才改立場；最多 3 輪，未收斂交給維護者' },
    { title: '比對', detail: '每輪比對兩份最新答案：一致就給結論與證據，該題結束；不一致列出分歧，未到第 3 輪就進下一輪。最多 3 輪，未收斂交給維護者，任一方都不得自行選邊。可由既有規則推出且雙方不推翻的題標「依規則定」，不交維護者' },
    { title: '摘要', detail: '一個 Claude 子代理把結果整理成最多 300 字的 issue_summary（每題結論、分歧點、要改的檔，不含本機絕對路徑），JS 檢查長度，超過就重寫一次，再超過就截斷；issue_note 是本機完整版（三段），workflow 不直接發 issue' },
  ],
}

// args:
//   round      string    必填，codex 輸出檔名用，例如 'q-exit-codes'；每輪的檔是 <round>-<id>-r<輪>.md
//   questions  array     必填，每題 { id, question, context }：id 用在檔名；context 寫現況、事實與已定案前提
//   background string    可省，所有題共用的已定案前提，不要質疑
//   repo       string    可省，要讀哪份檔的 repo 根目錄（絕對路徑）：內部對照、codex 的 --cd 與輸出位置；不給就用主 repo。
//                        要讀 PR worktree 的檔時明確帶。腳本（codex_run.py 等）不從這裡取，一律從主 repo 取
//   issues     number[]  可省，內部對照一定要讀的已定案 issue 編號（連留言）；另外會依題目關鍵字搜相關 issue
const { round, questions, background = '', repo: repoArg = '', issues = [] } = args ?? {}
if (typeof round !== 'string' || !round.trim()) throw new Error('args.round 必填')
if (!Array.isArray(questions) || questions.length === 0) throw new Error('args.questions 必填')
if (!Array.isArray(issues) || issues.some(x => !Number.isInteger(x) || x <= 0)) throw new Error(`args.issues 只能是正整數陣列（收到 ${JSON.stringify(issues)}）`)
log(`discuss ${round}`)

// 兩個值分開（#269）：
//   repo  讀哪份檔：內部對照、codex 的 --cd 與輸出位置；給了就照用，可以是舊分支的 worktree
//   main  腳本來源：主 repo 根目錄，script/workflow/ 一律從這裡取，舊分支沒有的腳本才不會找不到
// main 不寫死本機路徑：不論有沒有給 repo，都派子代理在 repo（沒給就用它的工作目錄）查 git common dir，
// 取它的上一層（在 linked worktree 也會回到主 repo）
const MAIN = {
  type: 'object',
  properties: {
    main: { type: 'string', description: '主 repo 根目錄的絕對路徑' },
    error: { type: 'string', description: '失敗原因；成功留空' },
  },
  required: ['main'],
}
const trimDir = x => (typeof x === 'string' ? x.trim().replace(/\/+$/, '') : '')
let repo = trimDir(repoArg)
if (repo && !repo.startsWith('/')) throw new Error(`args.repo 只能是絕對路徑（收到 ${JSON.stringify(repoArg)}）；不給就用主 repo`)
phase('準備')
const where = repo ? `在 ${repo} 執行（用 git -C）：

\`git -C ${repo} rev-parse --path-format=absolute --git-common-dir\`` : `在你的工作目錄執行：

\`git rev-parse --path-format=absolute --git-common-dir\``
const m = await agent(`只跑一個指令，不要改任何檔。${where}

它印出主 repo 的 .git 目錄（絕對路徑）。main 回報它的上一層目錄（去掉最後的 /.git），不要加結尾斜線。指令失敗或輸出不是以 /.git 結尾的絕對路徑時，main 留空字串，error 照抄輸出，不要自己補救。`,
  { label: `${round} 準備主 repo`, phase: '準備', schema: MAIN, agentType: 'general-purpose', effort: 'low' })
const main = trimDir(m?.main)
if (!main.startsWith('/')) throw new Error(`查不到主 repo：${m?.error || '子代理沒有回報絕對路徑'}`)
if (!repo) repo = main
const WF = `${main}/script/workflow`
log(`discuss ${round} repo ${repo}（讀檔、內部對照、codex --cd、輸出）`)
log(`discuss ${round} main ${main}（腳本 ${WF}）`)

// 內部對照（#359）：任何 codex／Claude 回答之前，先把已定案資料對照到每一題。
// 有些題其實能由既有規則推出，不該再送去問維護者；brief 也不再只靠主對話挑的條文。
const ISSUE_REPO = 'ycpss91255-research/vendor_kit'
const SEARCH_LIMIT = 5 // 依關鍵字搜相關 issue 時，每題最多讀幾個
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
      description: '每題一項，id 對應題目的 id',
      items: {
        type: 'object',
        properties: {
          id: { type: 'string' },
          basis: { type: 'array', items: BASIS_ITEM, description: '跟這題有關的已定依據；找不到就給空陣列，不要編' },
          derivable: { type: 'boolean', description: '能否只靠既有規則推出答案，不需要新的決定' },
          derived_answer: { type: 'string', description: 'derivable 為 true 時必填：推出的答案與推導（引用 basis 的出處）；false 時留空' },
          conflicts: { type: 'array', items: { type: 'string' }, description: '題目的前提或 context 與已定案內容衝突之處（附出處）；沒有就空陣列' },
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
const qList = questions.map(q => `- id: ${q.id}\n  問題：${q.question}\n  現況與事實：${q.context ?? ''}`).join('\n')
const internal = await agent(`只讀，不要改任何檔、不要發 issue 或留言。你的工作是在討論開始前，把已定案的內部資料對照到每一題。

repo 根目錄：${repo}（以下路徑都相對於它）

依序讀這些已定案資料；候選路徑照順序試，第一個存在的就用，不存在的每個都記進 missing，不要因此失敗：
1. 對外契約頁，每頁先試 doc/contract/<頁>，找不到再試 doc/decisions/review/<頁>；頁：${PAGES.join('、')}
2. doc/contract/reason_codes.csv
3. 名詞：根目錄 GLOSSARY.md，找不到再試 CONTEXT.md
4. doc/adr/*.md 全部（README.md 也讀，它是規則）
5. scope_roadmap.md：用 \`find ${repo} -name scope_roadmap.md -not -path '*/node_modules/*' -not -path '*/.git/*'\` 找，全部讀
6. 已定案 issue：${issues.length ? issues.map(n => `\`gh issue view ${n} -R ${ISSUE_REPO} --comments\``).join('、') : '（args.issues 沒給）'}
7. 相關 issue：每題取兩三個關鍵字跑 \`gh search issues "<關鍵字>" -R ${ISSUE_REPO} --limit ${SEARCH_LIMIT} --json number,title,state\`，每題最多讀 ${SEARCH_LIMIT} 個看起來相關的（\`gh issue view <N> -R ${ISSUE_REPO} --comments\`）；issue 本文開好後不改，新決定在留言，兩者都要看

題目：
${qList}

對每一題回報一項（id 照抄）：
- basis：跟這題有關的已定依據，每項 { source, says }。source 用 repo 相對檔名:行號（例如 doc/decisions/review/02_invariants.md:42），或 #<issue> 本文／#<issue> 留言（作者、日期）；says 一句話。只列真的讀到的，不要編、不要寫本機絕對路徑。
- derivable：只靠上面的既有規則就能推出答案、不需要新的決定（也不改對外承諾）時填 true；要新的取捨、規則沒涵蓋或規則彼此衝突時填 false。
- derived_answer：derivable 為 true 時必填，寫推出的答案與推導，引用 basis 的出處；false 時留空字串。
- conflicts：題目的前提或現況描述與已定案內容衝突就列出（附出處），沒有就空陣列。

read 列實際讀到的檔與 issue，missing 列嘗試過但不存在的路徑。整個對照做不下去（例如 repo 不存在）才填 error。`,
  { label: `${round} 內部對照`, phase: '內部對照', schema: INTERNAL })
if (!internal || (internal.error && !(Array.isArray(internal.items) && internal.items.length))) {
  throw new Error(`內部對照失敗：${internal?.error || '子代理沒有回報'}`)
}
const strs = xs => (Array.isArray(xs) ? xs.filter(x => typeof x === 'string' && x.trim()).map(x => x.trim()) : [])
const basisOf = new Map()
for (const q of questions) {
  const x = (Array.isArray(internal.items) ? internal.items : []).find(i => i && i.id === q.id)
  if (!x) log(`discuss ${round} 內部對照沒有回報 ${q.id}，該題當作沒有依據、不可由規則推出`)
  const basis = (Array.isArray(x?.basis) ? x.basis : [])
    .filter(b => b && typeof b.source === 'string' && b.source.trim())
    .map(b => ({ source: b.source.trim(), says: typeof b.says === 'string' ? b.says.trim() : '' }))
  const derived_answer = typeof x?.derived_answer === 'string' ? x.derived_answer.trim() : ''
  let derivable = x?.derivable === true
  if (derivable && (!derived_answer || basis.length === 0)) {
    log(`discuss ${round} ${q.id} 標了可由規則推出但沒有 derived_answer 或 basis，改當不可推出`)
    derivable = false
  }
  basisOf.set(q.id, { id: q.id, basis, derivable, derived_answer: derivable ? derived_answer : '', conflicts: strs(x?.conflicts) })
}
log(`discuss ${round} 內部對照：讀到 ${strs(internal.read).length} 份，不存在 ${strs(internal.missing).length} 個，可由規則推出 ${[...basisOf.values()].filter(b => b.derivable).length} 題`)

const BG = background.trim() ? `已定案前提（不要質疑）：\n${background.trim()}` : ''
const READ = '需要更多依據時，再讀題目提到的檔與已定案資料。已定案的決定記在 wayfinder map issue：跑 `gh issue view 78 -R ycpss91255-research/vendor_kit --comments`，本文的「Decisions so far」凍結不改、之後的新決定在留言，兩者都讀；要某條決定的細節，跑 `gh issue view <child> -R ycpss91255-research/vendor_kit --comments` 讀該 child issue 的留言（結論在留言裡）。只讀，不要發 issue 或留言。結論跟任何一條定案衝突時要明講是哪一條（#<child>）。結論要附證據（檔名＋行號、外部文件網址或 repo 內實例），沒有證據的主張標明是推論。'

// 內部對照的結果：每一輪、codex 與 Claude 都拿到同一份，當作不可質疑的前提
const basisText = q => {
  const b = basisOf.get(q.id)
  const lines = b.basis.length
    ? b.basis.map(x => `- ${x.source}：${x.says}`).join('\n')
    : '- （內部對照沒有找到這題的依據；你要自己查已定案資料，查過仍沒有就在 internal_basis 寫明查過哪些檔、沒有相關條文）'
  const derived = b.derivable
    ? `內部對照判定：這題可由既有規則推出，推出的答案：${b.derived_answer}\n要推翻它必須指出哪條依據讀錯或不適用，並附證據。`
    : '內部對照判定：這題不能只靠既有規則推出。'
  const conflicts = b.conflicts.length ? `\n題目前提與已定案內容的衝突：\n${b.conflicts.map(x => `- ${x}`).join('\n')}` : ''
  return `內部依據（已定案資料，由「內部對照」階段整理；這是不可質疑的前提）：
${lines}
${derived}${conflicts}

先引用內部依據，再談外部前例；與內部依據衝突要明講是哪一條。`
}

const ANSWER = {
  type: 'object',
  properties: {
    internal_basis: { type: 'array', items: { type: 'string' }, description: '這個結論引用的內部依據，每條「出處（repo 相對檔名:行號或 #issue 留言）：一句話」；不得為空' },
    answer: { type: 'string', description: '結論，一到三句' },
    reasons: { type: 'array', items: { type: 'string' }, description: '理由，每條附證據；先內部依據，再外部前例' },
    risks: { type: 'array', items: { type: 'string' }, description: '這個結論的風險或反例' },
    error: { type: 'string', description: '失敗原因；成功留空' },
  },
  required: ['internal_basis', 'answer', 'reasons', 'risks'],
}
const VERDICT = {
  type: 'object',
  properties: {
    id: { type: 'string' },
    agree: { type: 'boolean', description: '兩份最新結論是否一致' },
    derived_upheld: { type: 'boolean', description: '內部對照判定可由規則推出時：兩份最新結論都沒有推翻推出的答案就 true；不可推出、任一方推翻或任一方有 error 時 false' },
    conclusion: { type: 'string', description: '一致時的共同結論；不一致時寫各自立場' },
    evidence: { type: 'array', items: { type: 'string' } },
    disagreements: { type: 'array', items: { type: 'string' } },
    ask_user: { type: 'string', description: '要問維護者的一句話（附建議選項）；兩邊一致而且不改對外承諾時可留空' },
    recommendation: { type: 'string', description: '不一致時：依雙方證據推薦維護者選哪個選項與理由，只供參考，不算定案；一致時留空' },
  },
  required: ['id', 'agree', 'derived_upheld', 'conclusion', 'evidence', 'disagreements', 'ask_user', 'recommendation'],
}

// 討論規則：Claude 與 codex 最多討論 MAX_ROUNDS 輪。第 1 輪各自獨立回答；之後每輪把對方最新立場
// 交給雙方回應，直到一致或到第 MAX_ROUNDS 輪為止。到上限仍有分歧就停，列進「要維護者決定」，
// 任一方（含比對代理）都不得自行選邊；推薦只供維護者參考。
const MAX_ROUNDS = 3

// brief 的本體：第 1 輪只有題目與內部依據；第 2 輪起附上自己上一輪的答案與對方最新立場。
// retry 是 internal_basis 為空後的重試，要明講上一次為什麼無效
const brief = (q, n, own, other, otherName, retry) => {
  const base = `${BG}

問題：${q.question}

現況與事實：
${q.context}

${basisText(q)}

${READ}${retry ? '\n\n你上一次的回答沒有引用任何內部依據，被判為無效。這次必須先列出內部依據（出處＋一句話），再給結論。' : ''}`
  if (n === 1) return base
  return `${base}

這是第 ${n} 輪（最多 ${MAX_ROUNDS} 輪）。你上一輪的答案：
${JSON.stringify(own)}

${otherName} 的最新立場：
${JSON.stringify(other)}

逐條回應 ${otherName} 的理由：對方的證據成立就修正你的結論，不成立就指出錯在哪、附證據維持原結論。不要為了達成一致而讓步；沒有新證據就不要改立場。輸出你這一輪的完整答案。`
}

const codexAsk = (q, n, own, other, attempt) => agent(`你的工作是啟動 codex 回答一個設計問題，再把輸出整理成結構化回報。不要自己回答、不要改任何檔。

步驟：
1. 把下面的 brief 原文用 Write 工具寫進你的 scratchpad 暫存檔（不要用 heredoc）。
2. 前景執行（Bash timeout 600000，不要 run_in_background）：

python3 ${WF}/codex_run.py --cd ${repo} --brief <暫存檔> --out ${repo}/doc/decisions/review_log/codex/${round}-${q.id}-r${n}${attempt > 1 ? `-retry${attempt - 1}` : ''}.md

   - 腳本自己建輸出目錄、stdin 接 /dev/null、不帶沙箱旗標；不要繞過腳本直接呼叫 codex。
3. 讀腳本輸出的一行 JSON。ok 為 true：讀輸出檔，整理成 internal_basis／answer／reasons／risks。internal_basis 只從輸出檔的「內部依據」一節照抄，不要自己補、不要從別節推；那一節不存在或是空的，internal_basis 就給空陣列。ok 為 false：error 寫 JSON 的 exit、error 與 stderr_tail，其餘欄位留空字串或空陣列，不要編內容。

brief：
只讀，不要改任何檔。我要的是你的獨立判斷，不是背書。

${brief(q, n, own, other, 'Claude', attempt > 1)}

輸出 markdown，依序四節：內部依據（每條「出處：一句話」，不得為空）、結論（一到三句）、理由（每條附證據，先內部依據再外部前例）、風險或反例。不要客套話。`,
  { label: `${round} ${q.id} codex r${n}${attempt > 1 ? ' 重試' : ''}`, phase: n === 1 ? '各自回答' : '回應', schema: ANSWER, agentType: 'general-purpose' })

const claudeAsk = (q, n, own, other, attempt) => agent(`只讀，不要改任何檔。${n === 1 ? '獨立回答' : '回應'}下面的設計問題。internal_basis 必填且不得為空：列出你引用的內部依據（出處＋一句話）。

${brief(q, n, own, other, 'codex', attempt > 1)}`,
  { label: `${round} ${q.id} claude r${n}${attempt > 1 ? ' 重試' : ''}`, phase: n === 1 ? '各自回答' : '回應', schema: ANSWER })

// internal_basis 空的回答視為該輪無效：重試一次，仍空就把 error 記上（比對時算沒有結果）
const hasBasis = x => strs(x?.internal_basis).length > 0
const withBasis = async (name, q, n, ask) => {
  let x = await ask(1)
  if (x && !x.error && !hasBasis(x)) {
    log(`discuss ${round} ${q.id} r${n} ${name} 沒有引用內部依據，重試一次`)
    x = await ask(2)
  }
  if (x && !x.error && !hasBasis(x)) return { ...x, error: `${name} 第 ${n} 輪的 internal_basis 為空（重試一次仍空），該輪無效` }
  return x
}

const compare = (q, n, c, a) => {
  const b = basisOf.get(q.id)
  return agent(`比對兩份對同一個問題的最新答案（第 ${n} 輪，最多 ${MAX_ROUNDS} 輪）。不要加入新的立場；只判斷兩份是否一致、共同結論是什麼、分歧在哪。

問題：${q.question}

${b.derivable ? `內部對照判定這題可由既有規則推出，推出的答案：${b.derived_answer}` : '內部對照判定這題不能只靠既有規則推出。'}

codex：
${JSON.stringify(c)}

Claude：
${JSON.stringify(a)}

id 填 ${q.id}。任一份有 error（或缺結果）時 agree 填 false，並在 disagreements 寫哪一方沒有結果與原因。
derived_upheld：內部對照判定可由規則推出，而且兩份最新結論都沒有推翻推出的答案時填 true；不可推出、任一方推翻或任一方有 error 時填 false。
ask_user：兩份一致而且不改對外承諾時留空；否則寫成一句要問維護者的話，附建議選項（建議的放第一個）。
recommendation：不一致時依雙方證據寫推薦的選項與理由，只供維護者參考；你不能替維護者定案，也不能把分歧寫成一致。一致時留空。
你只回報，不要跑 gh 發 issue 或留言。`,
    { label: `${round} ${q.id} 比對 r${n}`, phase: '比對', schema: VERDICT })
}

// 單題討論：一致就停；不一致且未到上限就把對方最新立場交給雙方再答一輪
const discussOne = async q => {
  let c = null
  let a = null
  let v = null
  let n = 0
  const errors = []
  while (n < MAX_ROUNDS) {
    n += 1
    const [nc, na] = await parallel([
      () => withBasis('codex', q, n, attempt => codexAsk(q, n, c, a, attempt)),
      () => withBasis('Claude', q, n, attempt => claudeAsk(q, n, a, c, attempt)),
    ])
    c = nc
    a = na
    for (const x of [c, a]) if (x?.error) errors.push(x.error)
    v = await compare(q, n, c, a)
    if (!v || v.agree) break
  }
  if (!v) return null
  const b = basisOf.get(q.id)
  const agree = v.agree === true
  // 依規則定：內部對照判定可推出，雙方一致、都有結果，且比對確認雙方都沒有推翻推出的答案
  const by_rule = agree && b.derivable && v.derived_upheld === true && !!c && !!a && !c.error && !a.error
  return { ...v, id: q.id, question: q.question, rounds: n, agree, by_rule, internal: b, codex: c, claude: a, errors }
}

const results = (await parallel(questions.map(q => () => discussOne(q)))).filter(Boolean)

// issue_note 是本機完整版（給主對話與本機紀錄看），由腳本組，保證三段結構；
// 貼 issue 的是下面的 issue_summary。第 MAX_ROUNDS 輪後仍分歧的一律進「要維護者決定」
const list = xs => (Array.isArray(xs) && xs.length ? xs.map(x => `  - ${x}`).join('\n') : '  - （無）')
const stance = (name, x) => {
  if (!x) return `- ${name}：沒有結果`
  if (x.error) return `- ${name}：沒有結果（${x.error}）`
  return `- ${name}：${x.answer}\n${list(x.reasons)}`
}
const conflictsOf = r => (r.internal.conflicts.length ? `\n\n題目前提與已定案內容的衝突：\n${list(r.internal.conflicts)}` : '')
const basisListOf = r => list(r.internal.basis.map(x => `${x.source}：${x.says}`))
const byRule = results.filter(r => r.by_rule)
const agreed = results.filter(r => r.agree && !r.by_rule)
const open = results.filter(r => !r.agree)
const byRulePart = byRule.length
  ? byRule.map(r => `### ${r.id}：${r.question}\n\n依規則定：第 ${r.rounds} 輪雙方一致，沒有推翻內部對照推出的答案。\n\n${r.conclusion}\n\n推出的答案：${r.internal.derived_answer}\n\n內部依據：\n${basisListOf(r)}${conflictsOf(r)}`).join('\n\n')
  : '（無）'
const agreedPart = agreed.length
  ? agreed.map(r => `### ${r.id}：${r.question}\n\n第 ${r.rounds} 輪一致。\n\n${r.conclusion}\n\n證據：\n${list(r.evidence)}\n\n內部依據：\n${basisListOf(r)}${conflictsOf(r)}`).join('\n\n')
  : '（無）'
const openPart = open.length
  ? open.map(r => `### ${r.id}：${r.question}\n\n討論 ${r.rounds} 輪仍分歧，交給維護者決定。\n\n問題：${r.ask_user || r.question}\n\n內部依據：\n${basisListOf(r)}${conflictsOf(r)}\n\n雙方最新立場與理由：\n${stance('codex', r.codex)}\n${stance('Claude', r.claude)}\n\n分歧：\n${list(r.disagreements)}\n\n推薦（僅供參考，不算定案）：${r.recommendation || '（無）'}`).join('\n\n')
  : '（無）'
const issue_note = `## 依既有規則定（不必問維護者）\n\n${byRulePart}\n\n## 一致的結論\n\n${agreedPart}\n\n## 要維護者決定\n\n${openPart}`
const errors = results.flatMap(r => r.errors.map(e => `${r.id}：${e}`))

// issue_summary：貼 issue 用，最多 SUMMARY_MAX 字（中文一字算一，標點空白也算），不含本機絕對路徑。
// 超過或含本機路徑就重寫一次；再不行就把路徑換掉、截斷並加 TRUNC
phase('摘要')
const SUMMARY_MAX = 300
const TRUNC = '…（完整內容見本機輸出檔）'
const len = s => Array.from(s).length
const ABS_PATH = /(^|[^\w.~-])\/(home|tmp|Users|root|mnt|media|var|opt|private)\/[^\s`'"）)]*/g
const relLocal = s => [repo, main].reduce((t, d) => t.split(`${d}/`).join('').split(d).join('.'), String(s ?? '').trim())
const hasAbs = s => new RegExp(ABS_PATH.source).test(s)
const summaryProblems = s => [
  ...(!s ? ['摘要是空的'] : []),
  ...(len(s) > SUMMARY_MAX ? [`長度 ${len(s)} 字，超過上限 ${SUMMARY_MAX}`] : []),
  ...(hasAbs(s) ? ['含本機絕對路徑'] : []),
]
const category = r => (r.by_rule ? '依規則定' : r.agree ? '一致' : '要維護者決定')
const compact = results.map(r => ({
  id: r.id,
  question: r.question,
  category: category(r),
  conclusion: r.conclusion,
  derived_answer: r.internal.derived_answer || undefined,
  disagreements: r.agree ? undefined : r.disagreements,
  ask_user: r.agree ? undefined : r.ask_user,
  conflicts: r.internal.conflicts.length ? r.internal.conflicts : undefined,
}))
const SUMMARY = {
  type: 'object',
  properties: {
    summary: { type: 'string', description: `issue 摘要，最多 ${SUMMARY_MAX} 字` },
    error: { type: 'string', description: '失敗原因；成功留空' },
  },
  required: ['summary'],
}
const summarize = (prev, problems) => agent(`把下面的討論結果整理成貼 issue 用的摘要。只整理，不要加入新的立場、不要讀檔、不要跑 gh。

規則：
- 最多 ${SUMMARY_MAX} 個字元（中文一字算一，英數、標點、空白、換行也各算一）。
- 內容：每題的結論（標明「依規則定」「一致」或「要維護者決定」）、分歧點、要改的檔（repo 相對路徑）。
- 不含本機絕對路徑（例如 /home/...）；提到檔案一律用 repo 相對路徑。
- 不要客套話、不要標題層級，用短條列。

討論結果：
${JSON.stringify(compact)}${prev ? `

你上一版摘要不合格（${problems.join('；')}），請重寫：
${prev}` : ''}`,
  { label: `${round} 摘要${prev ? ' 重寫' : ''}`, phase: '摘要', schema: SUMMARY })
let issue_summary = relLocal((await summarize())?.summary)
let problems = summaryProblems(issue_summary)
if (problems.length) {
  log(`discuss ${round} 摘要不合格（${problems.join('；')}），重寫一次`)
  const again = relLocal((await summarize(issue_summary || '（空）', problems))?.summary)
  if (again) issue_summary = again
  problems = summaryProblems(issue_summary)
}
if (!issue_summary) {
  // 摘要子代理兩次都沒有結果：由腳本組最小摘要，避免主對話拿到空字串
  issue_summary = results.map(r => `- ${r.id}：${category(r)}`).join('\n') || '（沒有結果）'
  errors.push('摘要子代理沒有回報，issue_summary 由腳本組成')
}
if (hasAbs(issue_summary)) issue_summary = issue_summary.replace(ABS_PATH, (all, pre) => `${pre}<本機路徑>`)
if (len(issue_summary) > SUMMARY_MAX) {
  log(`discuss ${round} 摘要重寫後仍有 ${len(issue_summary)} 字，截斷`)
  issue_summary = Array.from(issue_summary).slice(0, SUMMARY_MAX - len(TRUNC)).join('') + TRUNC
}

return {
  round,
  max_rounds: MAX_ROUNDS,
  issue_summary, // 貼 issue 用，最多 300 字
  issue_note, // 本機完整版（三段），不直接貼 issue
  internal: { read: strs(internal.read), missing: strs(internal.missing), items: [...basisOf.values()] },
  by_rule: byRule,
  agreed,
  ask_maintainer: open,
  results,
  errors,
}

// args 範例：
// {
//   "round": "q-exit-codes",
//   "background": "<所有題共用的已定案前提>",
//   "issues": [78, 123],
//   "questions": [
//     { "id": "exit-codes", "question": "<要問的設計問題>", "context": "<現況、事實與已定案前提>" }
//   ]
// }
