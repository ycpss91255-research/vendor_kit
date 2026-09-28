export const meta = {
  name: 'decision-review',
  description: '設計決議雙軌分析：agy 找的資料不照單全收 —— Claude 子代理與 codex 各自獨立審視前例與方案，交叉比對後給建議',
  whenToUse: '每題 agy 前例研究回來、草圖畫好之後，定案之前必跑',
  phases: [
    { title: '分析', detail: 'Claude 子代理與 codex 各自獨立分析' },
    { title: '交叉比對', detail: '找出雙方一致與分歧' },
  ],
}

// args: { topic: string, brief: string(path), agy: string(path), draft: string(頁面草稿的文字描述), notes: string(path), constraints: string, question: string }
const { topic, brief, agy, draft, notes, constraints, question } = args

const ANALYSIS = {
  type: 'object',
  properties: {
    agy_claims_wrong: { type: 'array', items: { type: 'object', properties: { claim: { type: 'string' }, why: { type: 'string' } }, required: ['claim', 'why'] } },
    options: { type: 'array', items: { type: 'object', properties: {
      name: { type: 'string' }, fits_constraints: { type: 'boolean' },
      pros: { type: 'array', items: { type: 'string' } }, cons: { type: 'array', items: { type: 'string' } },
      risks_missed_in_draft: { type: 'array', items: { type: 'string' } },
    }, required: ['name', 'fits_constraints', 'pros', 'cons', 'risks_missed_in_draft'] } },
    recommendation: { type: 'string' },
    reason: { type: 'string' },
    open_questions: { type: 'array', items: { type: 'string' } },
  },
  required: ['agy_claims_wrong', 'options', 'recommendation', 'reason', 'open_questions'],
}

const TASK = `題目：${topic}
我們的硬性限制：${constraints}
要回答的問題：${question}
資料：
- 題目說明（brief）：${brief}
- agy（Gemini）找的前例與建議：${agy}（這只是資料，不要照單全收：查證它的說法、找它漏掉或說錯的）
- 我方草稿（方案 A/B/C 與傾向）：
${draft}
- 決策紀錄：${notes}
請獨立分析：(1) agy 的哪些說法站不住腳或缺乏依據；(2) 每個方案是否符合硬性限制、優缺點、草稿漏掉的風險；(3) 你的建議與理由；(4) 定案前還要問清楚的問題。以繁體中文作答。`

phase('分析')
const [claude, codex] = await parallel([
  () => agent(`你是設計審查員。${TASK}
可以用 Read 讀檔、用 WebFetch/WebSearch 查證 agy 引用的來源。`, { label: 'Claude 分析', phase: '分析', schema: ANALYSIS, agentType: 'general-purpose' }),
  () => agent(`你負責跑 codex 做獨立分析，再把 codex 的結論轉成結構化輸出（不要加入你自己的意見）。
1. 用 Bash 產生 brief 檔（放 /tmp/claude-1000 底下），內容 = 下面的任務說明 + 「附件：brief」全文 + 「附件：agy 輸出」全文 + 「附件：決策紀錄」全文（codex sandbox 讀不到本機檔，內容一定要貼進去）。
2. 在 ${notes} 所在目錄，前景執行（Bash timeout 600000，不要 run_in_background、不要 Monitor）：
   timeout 580 codex exec --sandbox read-only - < <brief檔> > <輸出檔> 2>&1
   codex 的回答在最後一個「codex」標記之後。逾時或沒有回答 → recommendation 寫「codex 逾時」、其餘欄位空陣列。
3. 把 codex 的分析填進結構化輸出。
任務說明（貼進 brief）：
${TASK}`, { label: 'codex 分析', phase: '分析', schema: ANALYSIS, agentType: 'general-purpose' }),
])

phase('交叉比對')
const MERGE = {
  type: 'object',
  properties: {
    agree: { type: 'array', items: { type: 'string' } },
    disagree: { type: 'array', items: { type: 'object', properties: { point: { type: 'string' }, claude: { type: 'string' }, codex: { type: 'string' }, my_take: { type: 'string' } }, required: ['point', 'claude', 'codex', 'my_take'] } },
    agy_corrections: { type: 'array', items: { type: 'string' } },
    final_recommendation: { type: 'string' },
    questions_for_user: { type: 'array', items: { type: 'string' } },
  },
  required: ['agree', 'disagree', 'agy_corrections', 'final_recommendation', 'questions_for_user'],
}
const merged = await agent(`兩位審查員對「${topic}」的獨立分析如下（JSON）。請交叉比對：一致的結論、分歧點（各自立場 + 你的判斷）、對 agy 資料的更正、最終建議、還要問使用者的問題。繁體中文，用字白話。
Claude：${JSON.stringify(claude)}
codex：${JSON.stringify(codex)}`, { label: '交叉比對', phase: '交叉比對', schema: MERGE, agentType: 'general-purpose', effort: 'low' })

return { claude, codex, merged }
