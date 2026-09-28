export const meta = {
  name: 'diagram-review-claude',
  description: '單軌版（codex 不可用時）：兩個獨立 Claude 子代理看圖，只有一方提出的逐條驗證',
  whenToUse: '每次改完 dist_distribution.drawio 之後，交付前必跑',
  phases: [
    { title: '審查', detail: '兩個 Claude 子代理各自獨立審查' },
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
const [claude, codex] = await parallel([  // codex 變數在此版 = 第二位 Claude
  () => agent(`你是圖面審查員。用 Read 工具逐一看這些 PNG（白底）：
${pageList}
draw.io XML：${xml}（未壓縮，可 grep cell id）；決策紀錄：${notes}。
本輪改動：${changes}
${focus ? '特別注意：' + focus : ''}
${CRITERIA}
逐頁找問題。第一次看、沒有背景的人看不懂的地方也算問題（可讀性）。只回報真正的問題，不要建議改設計。`,
    { label: 'Claude 看圖', phase: '審查', schema: FINDINGS, agentType: 'general-purpose' }),

  () => agent(`你是第二位圖面審查員（獨立作業，不知道另一位的結果）。用 Read 工具逐一看這些 PNG（白底）：
${pageList}
draw.io XML：${xml}（未壓縮，可 grep cell id）；決策紀錄：${notes}。
本輪改動：${changes}
${focus ? '特別注意：' + focus : ''}
${CRITERIA}
逐頁找問題，優先找「內容與 notes 矛盾」與「流程缺線／缺分支」。只回報真正的問題，不要建議改設計。`,
    { label: 'Claude 看圖 B', phase: '審查', schema: FINDINGS, agentType: 'general-purpose' }),
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
