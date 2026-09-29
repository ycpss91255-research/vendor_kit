export const meta = {
  name: 'discuss',
  description: '維護者還沒回覆的問題先跟 codex 討論：codex 與 Claude 各自獨立回答，再比對出共識與分歧，整理成要問維護者的一句話',
  whenToUse: '有問題要問維護者之前；結果寫進 doc/decisions/review_log/discussion_queue.md 再依序問',
  phases: [
    { title: '各自回答', detail: '每題 codex（只讀）與 Claude 子代理各答一次，互不知道對方的答案' },
    { title: '比對', detail: '比對兩份答案：一致就給結論與證據；不一致列出分歧，整理成要問維護者的問題' },
  ],
}

// args:
//   round      string  必填，codex 輸出檔名用，例如 'q-2026-09-30'
//   questions  array   必填，每題 { id, question, context }：id 用在檔名；context 寫現況、事實與已定案前提
//   background string  可省，所有題共用的已定案前提，不要質疑
const { round, questions, background = '' } = args ?? {}
if (typeof round !== 'string' || !round.trim()) throw new Error('args.round 必填')
if (!Array.isArray(questions) || questions.length === 0) throw new Error('args.questions 必填')

const repo = '/home/cyc/Desktop/vendor-kit_ws/src'
const BG = background.trim() ? `已定案前提（不要質疑）：\n${background.trim()}` : ''
const READ = '先讀 CONTEXT.md、doc/decisions/review/01_purpose.md、doc/decisions/review/02_invariants.md，以及題目提到的檔；結論要附證據（檔名＋行號、外部文件網址或 repo 內實例），沒有證據的主張標明是推論。'

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
    agree: { type: 'boolean', description: '兩份結論是否一致' },
    conclusion: { type: 'string', description: '一致時的共同結論；不一致時寫各自立場' },
    evidence: { type: 'array', items: { type: 'string' } },
    disagreements: { type: 'array', items: { type: 'string' } },
    ask_user: { type: 'string', description: '要問維護者的一句話（附建議選項）；兩邊一致而且不改對外承諾時可留空' },
  },
  required: ['id', 'agree', 'conclusion', 'evidence', 'disagreements', 'ask_user'],
}

const codexAsk = q => agent(`你的工作是啟動 codex 回答一個設計問題，再把輸出整理成結構化回報。不要自己回答、不要改任何檔。

步驟：
1. \`mkdir -p ${repo}/doc/decisions/review_log/codex\`
2. 把下面的 brief 原文用 heredoc（'EOF'）寫進你的 scratchpad 暫存檔。
3. 前景執行（Bash timeout 600000，不要 run_in_background），形狀一字不差：

codex exec --skip-git-repo-check -C ${repo} -o ${repo}/doc/decisions/review_log/codex/${round}-${q.id}.md "$(cat <暫存檔>)" < /dev/null

   - \`< /dev/null\` 不可省略；不要帶 --sandbox。
4. 讀輸出檔，整理成 answer／reasons／risks。codex 失敗或輸出是空的：error 寫原因，其餘欄位留空字串或空陣列，不要編內容。

brief：
只讀，不要改任何檔。我要的是你的獨立判斷，不是背書。

${BG}

問題：${q.question}

現況與事實：
${q.context}

${READ}

輸出 markdown：結論（一到三句）、理由（每條附證據）、風險或反例。不要客套話。`,
  { label: `codex:${q.id}`, phase: '各自回答', schema: ANSWER, agentType: 'general-purpose' })

const claudeAsk = q => agent(`只讀，不要改任何檔。獨立回答下面的設計問題。

${BG}

問題：${q.question}

現況與事實：
${q.context}

${READ}`,
  { label: `claude:${q.id}`, phase: '各自回答', schema: ANSWER })

const results = await pipeline(
  questions,
  q => parallel([() => codexAsk(q), () => claudeAsk(q)]),
  ([c, a], q) => agent(`比對兩份對同一個問題的獨立答案。不要加入新的立場；只判斷兩份是否一致、共同結論是什麼、分歧在哪。

問題：${q.question}

codex：
${JSON.stringify(c)}

Claude：
${JSON.stringify(a)}

id 填 ${q.id}。ask_user：兩份一致而且不改對外承諾時留空；否則寫成一句要問維護者的話，附建議選項（建議的放第一個）。codex 那份有 error 時 agree 填 false，並在 disagreements 寫 codex 沒有結果。`,
    { label: `比對:${q.id}`, phase: '比對', schema: VERDICT }),
)
return results.filter(Boolean)
