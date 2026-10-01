export const meta = {
  name: 'discuss',
  description: 'codex 與 Claude 各自回答、最多 3 輪比對，未收斂交維護者',
  whenToUse: '問維護者之前；結果回報主對話，貼到 #78 對應的 child issue',
  phases: [
    { title: '各自回答', detail: '第 1 輪：每題 codex（只讀）與 Claude 子代理各答一次，互不知道對方的答案' },
    { title: '回應', detail: '第 2、3 輪：上一輪不一致的題，把對方最新立場交給雙方各自回應，證據成立才改立場；最多 3 輪，未收斂交給維護者' },
    { title: '比對', detail: '每輪比對兩份最新答案：一致就給結論與證據，該題結束；不一致列出分歧，未到第 3 輪就進下一輪。最多 3 輪，未收斂交給維護者，任一方都不得自行選邊。最後整理成 issue_note（「一致的結論」與「要維護者決定」兩段）給主對話貼到 issue（workflow 不直接發 issue）' },
  ],
}

// args:
//   round      string  必填，codex 輸出檔名用，例如 'q-exit-codes'；每輪的檔是 <round>-<id>-r<輪>.md
//   questions  array   必填，每題 { id, question, context }：id 用在檔名；context 寫現況、事實與已定案前提
//   background string  可省，所有題共用的已定案前提，不要質疑
const { round, questions, background = '', repo = '/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59' } = args ?? {}
if (typeof round !== 'string' || !round.trim()) throw new Error('args.round 必填')
if (!Array.isArray(questions) || questions.length === 0) throw new Error('args.questions 必填')
log(`discuss ${round}`)

const BG = background.trim() ? `已定案前提（不要質疑）：\n${background.trim()}` : ''
const READ = '先讀 GLOSSARY.md、doc/contract/01_purpose.md、doc/contract/02_invariants.md，以及題目提到的檔。已定案的決定記在 wayfinder map issue：跑 `gh issue view 78 -R ycpss91255-research/vendor_kit --comments`，本文的「Decisions so far」凍結不改、之後的新決定在留言，兩者都讀；要某條決定的細節，跑 `gh issue view <child> -R ycpss91255-research/vendor_kit --comments` 讀該 child issue 的留言（結論在留言裡）。只讀，不要發 issue 或留言。結論跟任何一條定案衝突時要明講是哪一條（#<child>）。結論要附證據（檔名＋行號、外部文件網址或 repo 內實例），沒有證據的主張標明是推論。'

const ANSWER = {
  type: 'object',
  properties: {
    answer: { type: 'string', description: '結論，一到三句' },
    reasons: { type: 'array', items: { type: 'string' }, description: '理由，每條附證據' },
    risks: { type: 'array', items: { type: 'string' }, description: '這個結論的風險或反例' },
    error: { type: 'string', description: '失敗原因；成功留空' },
  },
  required: ['answer', 'reasons', 'risks'],
}
const VERDICT = {
  type: 'object',
  properties: {
    id: { type: 'string' },
    agree: { type: 'boolean', description: '兩份最新結論是否一致' },
    conclusion: { type: 'string', description: '一致時的共同結論；不一致時寫各自立場' },
    evidence: { type: 'array', items: { type: 'string' } },
    disagreements: { type: 'array', items: { type: 'string' } },
    ask_user: { type: 'string', description: '要問維護者的一句話（附建議選項）；兩邊一致而且不改對外承諾時可留空' },
    recommendation: { type: 'string', description: '不一致時：依雙方證據推薦維護者選哪個選項與理由，只供參考，不算定案；一致時留空' },
  },
  required: ['id', 'agree', 'conclusion', 'evidence', 'disagreements', 'ask_user', 'recommendation'],
}

// 討論規則：Claude 與 codex 最多討論 MAX_ROUNDS 輪。第 1 輪各自獨立回答；之後每輪把對方最新立場
// 交給雙方回應，直到一致或到第 MAX_ROUNDS 輪為止。到上限仍有分歧就停，列進「要維護者決定」，
// 任一方（含比對代理）都不得自行選邊；推薦只供維護者參考。
const MAX_ROUNDS = 3

// brief 的本體：第 1 輪只有題目；第 2 輪起附上自己上一輪的答案與對方最新立場
const brief = (q, n, own, other, otherName) => {
  const base = `${BG}

問題：${q.question}

現況與事實：
${q.context}

${READ}`
  if (n === 1) return base
  return `${base}

這是第 ${n} 輪（最多 ${MAX_ROUNDS} 輪）。你上一輪的答案：
${JSON.stringify(own)}

${otherName} 的最新立場：
${JSON.stringify(other)}

逐條回應 ${otherName} 的理由：對方的證據成立就修正你的結論，不成立就指出錯在哪、附證據維持原結論。不要為了達成一致而讓步；沒有新證據就不要改立場。輸出你這一輪的完整答案。`
}

const codexAsk = (q, n, own, other) => agent(`你的工作是啟動 codex 回答一個設計問題，再把輸出整理成結構化回報。不要自己回答、不要改任何檔。

步驟：
1. \`mkdir -p ${repo}/doc/decisions/review_log/codex\`
2. 把下面的 brief 原文用 heredoc（'EOF'）寫進你的 scratchpad 暫存檔。
3. 前景執行（Bash timeout 600000，不要 run_in_background），形狀一字不差：

codex exec --skip-git-repo-check -C ${repo} -o ${repo}/doc/decisions/review_log/codex/${round}-${q.id}-r${n}.md "$(cat <暫存檔>)" < /dev/null

   - \`< /dev/null\` 不可省略；不要帶 --sandbox。
4. 讀輸出檔，整理成 answer／reasons／risks。codex 失敗或輸出是空的：error 寫原因，其餘欄位留空字串或空陣列，不要編內容。

brief：
只讀，不要改任何檔。我要的是你的獨立判斷，不是背書。

${brief(q, n, own, other, 'Claude')}

輸出 markdown：結論（一到三句）、理由（每條附證據）、風險或反例。不要客套話。`,
  { label: `${round} ${q.id} codex r${n}`, phase: n === 1 ? '各自回答' : '回應', schema: ANSWER, agentType: 'general-purpose' })

const claudeAsk = (q, n, own, other) => agent(`只讀，不要改任何檔。${n === 1 ? '獨立回答' : '回應'}下面的設計問題。

${brief(q, n, own, other, 'codex')}`,
  { label: `${round} ${q.id} claude r${n}`, phase: n === 1 ? '各自回答' : '回應', schema: ANSWER })

const compare = (q, n, c, a) => agent(`比對兩份對同一個問題的最新答案（第 ${n} 輪，最多 ${MAX_ROUNDS} 輪）。不要加入新的立場；只判斷兩份是否一致、共同結論是什麼、分歧在哪。

問題：${q.question}

codex：
${JSON.stringify(c)}

Claude：
${JSON.stringify(a)}

id 填 ${q.id}。ask_user：兩份一致而且不改對外承諾時留空；否則寫成一句要問維護者的話，附建議選項（建議的放第一個）。codex 那份有 error 時 agree 填 false，並在 disagreements 寫 codex 沒有結果。
recommendation：不一致時依雙方證據寫推薦的選項與理由，只供維護者參考；你不能替維護者定案，也不能把分歧寫成一致。一致時留空。
你只回報，不要跑 gh 發 issue 或留言。`,
  { label: `${round} ${q.id} 比對 r${n}`, phase: '比對', schema: VERDICT })

// 單題討論：一致就停；不一致且未到上限就把對方最新立場交給雙方再答一輪
const discussOne = async q => {
  let c = null
  let a = null
  let v = null
  let n = 0
  while (n < MAX_ROUNDS) {
    n += 1
    const [nc, na] = await parallel([() => codexAsk(q, n, c, a), () => claudeAsk(q, n, a, c)])
    c = nc
    a = na
    v = await compare(q, n, c, a)
    if (!v || v.agree) break
  }
  if (!v) return null
  return { ...v, id: q.id, question: q.question, rounds: n, agree: v.agree === true, codex: c, claude: a }
}

const results = (await parallel(questions.map(q => () => discussOne(q)))).filter(Boolean)

// issue_note 由腳本組，保證兩段結構；第 MAX_ROUNDS 輪後仍分歧的一律進「要維護者決定」
const list = xs => (Array.isArray(xs) && xs.length ? xs.map(x => `  - ${x}`).join('\n') : '  - （無）')
const stance = (name, x) => {
  if (!x) return `- ${name}：沒有結果`
  if (x.error) return `- ${name}：沒有結果（${x.error}）`
  return `- ${name}：${x.answer}\n${list(x.reasons)}`
}
const agreed = results.filter(r => r.agree)
const open = results.filter(r => !r.agree)
const agreedPart = agreed.length
  ? agreed.map(r => `### ${r.id}：${r.question}\n\n第 ${r.rounds} 輪一致。\n\n${r.conclusion}\n\n證據：\n${list(r.evidence)}`).join('\n\n')
  : '（無）'
const openPart = open.length
  ? open.map(r => `### ${r.id}：${r.question}\n\n討論 ${r.rounds} 輪仍分歧，交給維護者決定。\n\n問題：${r.ask_user || r.question}\n\n雙方最新立場與理由：\n${stance('codex', r.codex)}\n${stance('Claude', r.claude)}\n\n分歧：\n${list(r.disagreements)}\n\n推薦（僅供參考，不算定案）：${r.recommendation || '（無）'}`).join('\n\n')
  : '（無）'
const issue_note = `## 一致的結論\n\n${agreedPart}\n\n## 要維護者決定\n\n${openPart}`

return { round, max_rounds: MAX_ROUNDS, issue_note, agreed, ask_maintainer: open, results }

// args 範例：
// {
//   "round": "q-exit-codes",
//   "background": "<所有題共用的已定案前提>",
//   "questions": [
//     { "id": "exit-codes", "question": "<要問的設計問題>", "context": "<現況、事實與已定案前提>" }
//   ]
// }
