export const meta = {
  name: 'diagram-review',
  description: '對 draw.io 圖檔做雙軌審查：Claude 子代理看圖 + codex 獨立審查，交叉比對後逐條驗證',
  whenToUse: '每次改完 dist_distribution.drawio 之後，交付前必跑',
  phases: [
    { title: '審查', detail: 'Claude 子代理與 codex 各自獨立審查' },
    { title: '驗證', detail: '只有一方提出的項目，由第三個代理對照圖面確認' },
  ],
}

// args: { pngs: {page:string, path:string}[], xml: string, notes: string, changes: string, focus?: string }
const { pngs, xml, notes, changes, focus } = args
const pageList = pngs.map(p => `- ${p.path}（${p.page}）`).join('\n')

const FINDINGS = {
  type: 'object',
  properties: {
    findings: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          page: { type: 'string', description: '頁名' },
          id: { type: 'string', description: '元件或線段 id；找不到就寫元件上的文字' },
          category: { type: 'string', enum: ['排版', '顏色', '可讀性', '內容一致性'] },
          description: { type: 'string', description: '一句話說明問題' },
          must_fix: { type: 'boolean', description: '是否必須修才可交付' },
        },
        required: ['page', 'id', 'category', 'description', 'must_fix'],
      },
    },
    verdict: { type: 'string', enum: ['可以交付', '還不行'] },
  },
  required: ['findings', 'verdict'],
}

const CRITERIA = `審查標準（使用者定的）：
1. 架構圖只畫模組→最小單元與模組間傳的資料；流程圖另外分頁。
2. 顏色要有明確一致的意義，以各頁底部圖例為準；沒有的顏色不可出現。
3. 字要少，一般人（非工程師）也看得懂；專有名詞要在該頁底部「本頁名詞」表裡。
4. 線段：不穿無關方框、不交叉、不壓字、不裁切、不懸空、不該折的不折。
5. 線上文字 12pt。
6. 內容要跟 notes 的決策一致，且不可出現任何特定工具名（如 base）當實例，一律用 <repo>。
7. 每個方塊只放一件事（一個動作、一個判斷、一個檔案、一個最小單元）；一格裡有兩件事（例如「寫 A 並刪 B」「檢查 X 然後重生 Y」）就是問題，要拆成兩格。`

phase('審查')
const [claude, codex] = await parallel([
  () => agent(`你是圖面審查員。用 Read 工具逐一看這些 PNG（白底）：
${pageList}
draw.io XML：${xml}（未壓縮，可 grep cell id）；決策紀錄：${notes}。
本輪改動：${changes}
${focus ? '特別注意：' + focus : ''}
${CRITERIA}
逐頁找問題。第一次看、沒有背景的人看不懂的地方也算問題（可讀性）。只回報真正的問題，不要建議改設計。`,
    { label: 'Claude 看圖', phase: '審查', schema: FINDINGS, agentType: 'general-purpose' }),

  () => agent(`你負責跑 codex 做獨立審查，然後把 codex 的結論轉成結構化清單。步驟：
1. 用 Bash 產生 brief 檔（放在 /tmp/claude-1000 底下任何目錄），內容依序為：
   (a) 下面這段審查標準與本輪改動；(b) 「附件：決策紀錄」= ${notes} 的全文；(c) 「附件：drawio XML」= ${xml} 的全文（用 \`\`\`xml 包起來）。
   codex 的 sandbox 讀不到本機檔案，所以檔案內容一定要直接貼進 brief。
2. 執行（在 ${notes} 所在目錄）：
   timeout 580 codex exec --sandbox read-only ${pngs.map(p => '-i ' + p.path).join(' ')} - < <brief檔> > <輸出檔> 2>&1
   必須用 Bash 前景執行、timeout 參數設 600000；絕對不要 run_in_background，也不要用 Monitor 等待——你一結束回合，workflow 就會把你當作完成。
   跑完後讀取輸出檔。codex 的回答在最後一個「codex」標記之後、「tokens used」之前。若 codex 逾時或沒有回答，findings 回傳空陣列、verdict 寫「codex 逾時」。
3. 把 codex 指出的每個問題轉成 findings；codex 的最終判定放進 verdict。不要加入你自己的意見。

要貼進 brief 的審查標準與要求（請用繁體中文寫進去）：
${CRITERIA}
本輪改動：${changes}
${focus ? '特別注意：' + focus : ''}
要 codex 回答：逐頁列出 (A) 排版問題 (B) 顏色不符圖例 (C) 一般人看不懂的點與名詞表遺漏 (D) 與 notes 矛盾之處，每項給 id 與一句說明；最後給「可以交付」或「還不行」。附件 PNG 的頁次：${pngs.map(p => p.page).join('、')}。`,
    { label: 'codex 審查', phase: '審查', schema: FINDINGS, agentType: 'general-purpose' }),
])

const tag = (r, src) => (r?.findings ?? []).map(f => ({ ...f, sources: [src] }))
const all = [...tag(claude, 'claude'), ...tag(codex, 'codex')]
const key = f => `${f.page}|${f.id}|${f.category}`.toLowerCase()
const merged = new Map()
for (const f of all) {
  const k = key(f)
  if (merged.has(k)) merged.get(k).sources.push(...f.sources)
  else merged.set(k, { ...f })
}
const both = [...merged.values()].filter(f => new Set(f.sources).size === 2)
const single = [...merged.values()].filter(f => new Set(f.sources).size === 1)
log(`Claude ${claude?.findings?.length ?? 0} 項、codex ${codex?.findings?.length ?? 0} 項；雙方都提到 ${both.length} 項，只有一方提到 ${single.length} 項 → 逐條驗證`)

phase('驗證')
const VERDICT = {
  type: 'object',
  properties: { real: { type: 'boolean' }, reason: { type: 'string' } },
  required: ['real', 'reason'],
}
const verified = await pipeline(single,
  f => agent(`請對照圖面確認這個審查意見是否成立。圖：${pngs.find(p => p.page === f.page)?.path ?? pageList}；XML：${xml}（可 grep id）。
意見：[${f.page}] ${f.id}（${f.category}）：${f.description}
用 Read 看圖、必要時 grep XML。若圖上確實如此 → real=true；若意見錯誤或已不存在 → real=false。只判定，不擴充。`,
    { label: `驗證：${f.id}`, phase: '驗證', schema: VERDICT, agentType: 'general-purpose', effort: 'low' })
    .then(v => ({ ...f, real: v?.real ?? true, reason: v?.reason ?? '（驗證代理未回應，保守視為成立）' })))

const confirmed = [...both.map(f => ({ ...f, real: true })), ...verified.filter(Boolean).filter(f => f.real)]
const rejected = verified.filter(Boolean).filter(f => !f.real)
const byPage = {}
for (const f of confirmed) (byPage[f.page] ??= []).push(f)
return {
  verdict: { claude: claude?.verdict ?? '（無）', codex: codex?.verdict ?? '（無）' },
  confirmed: byPage,
  must_fix_count: confirmed.filter(f => f.must_fix).length,
  rejected: rejected.map(f => ({ page: f.page, id: f.id, description: f.description, reason: f.reason, source: f.sources[0] })),
}
