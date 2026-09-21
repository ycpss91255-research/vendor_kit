export const meta = {
  name: 'diagram-review-v2',
  description: '三階段 draw.io 審查：機械抽取＋lint 先跑好，代理只做內容／連接、排版（縮圖）、一格一事判定，最後逐條驗證',
  whenToUse: '每次改完 v2_only.drawio（或任何多頁流程圖）之後、交付前；主對話先跑 extract_pages.py → lint_pages.py → shrink_png.py',
  phases: [
    { title: '抽取', detail: '不跑 shell：只整理主對話先跑好的 extracted／lint／縮圖清單並分組' },
    { title: '內容與連接', detail: '4 組頁面平行：讀 <id>.md + lint.md 該頁段 + notes，找矛盾／缺分支／順序錯／lint 候選是否成立' },
    { title: '排版', detail: '每 10 頁縮圖一個代理，只找人眼才看得出的（標籤位置、可讀性、線太繞）' },
    { title: '其他', detail: '一個代理拿 lint 的「一格一事候選」逐格判定是否真的兩件事' },
    { title: '驗證', detail: '每條 finding 由 effort low 代理對照 md／縮圖確認' },
  ],
}

// args: {
//   extracted: string,                 // extract_pages.py 的輸出目錄（<id>.json／<id>.md／pages.json）
//   lint: string,                      // lint_pages.py 產的 lint.md 路徑
//   pngs: {page: string, path: string}[],   // shrink_png.py 產的縮圖清單（pngs.json 內容；page = 頁 id）
//   notes: string,                     // 決策紀錄檔路徑
//   changes: string,                   // 本輪改動說明
//   focus?: string,                    // 特別注意
//   pages?: string[],                  // 頁 id 白名單（只審這些頁）
//   lint_items?: {page,rule,level,id,msg}[],  // lint.json 內容（可選）；有給就原樣列進結果的 lint_mechanical
// }
const { extracted, lint, pngs, notes, changes, focus, pages, lint_items } = args
const CONTENT_GROUPS = 4      // 內容與連接：分幾組
const LAYOUT_CHUNK = 10       // 排版：每個代理幾頁縮圖

const allPages = (pngs ?? []).map(p => p.page)
const pageIds = pages && pages.length ? allPages.filter(p => pages.includes(p)) : allPages
const pngOf = id => (pngs ?? []).find(p => p.page === id)?.path
const mdOf = id => `${extracted}/${id}.md`
const chunk = (arr, n) => arr.reduce((acc, x, i) => ((acc[Math.floor(i / n)] ??= []).push(x), acc), [])
const split = (arr, k) => { const size = Math.ceil(arr.length / k) || 1; return chunk(arr, size) }

const FINDINGS = {
  type: 'object',
  properties: {
    findings: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          page: { type: 'string', description: '頁 id（例如 v1p5c，不是頁名）' },
          id: { type: 'string', description: '元件或線段 id；找不到就寫元件上的文字' },
          category: { type: 'string', enum: ['排版', '顏色', '可讀性', '內容一致性', 'lint'] },
          description: { type: 'string', description: '一句話說明問題；category=lint 時開頭寫 lint 規則代號（如 dangling／onething）' },
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

const MD_FORMAT = `<id>.md 的格式：「## nodes」每行 [kind/cls] id: 文字（kind = step／decision／end_ok 綠／end_orange 橙／end_red 紅／entry 白虛線入口／file／rule／header／note／term／other；⏎ = 換行）；
「## edges」每行 id: 來源(文字) --標籤--> 目標(文字)；「## terms」本頁名詞表；「## xrefs」跨頁引用。
lint.md 依頁分組（## <頁id> <頁名>），每行 [規則][warn|info] id: 說明；規則代號見檔頭。`

// ───────────────── 抽取 ─────────────────
phase('抽取')
if (!pageIds.length) throw new Error('沒有可審的頁：請確認 args.pngs（shrink_png.py 的 pngs.json）與 args.pages')
const missingMd = pageIds.filter(id => !pngOf(id))
if (missingMd.length) log(`注意：${missingMd.length} 頁沒有縮圖：${missingMd.join('、')}`)
const contentGroups = split(pageIds, CONTENT_GROUPS)
const layoutGroups = chunk(pageIds, LAYOUT_CHUNK)
log(`共 ${pageIds.length} 頁（${pages?.length ? '白名單' : '全部'}）；內容與連接 ${contentGroups.length} 組、排版 ${layoutGroups.length} 組（每組 ≤ ${LAYOUT_CHUNK} 頁）；lint：${lint}`)

// ───────────────── 三個找問題的階段：各自獨立、找到的 findings 立刻進驗證（pipeline，無 barrier） ─────────────────
const finders = [
  ...contentGroups.map((ids, i) => ({
    kind: '內容與連接', label: `內容與連接 ${i + 1}/${contentGroups.length}`, ids,
    prompt: `你是流程圖內容審查員（第 ${i + 1} 組，共 ${contentGroups.length} 組）。不看圖片，只讀文字抽取結果。
你這組的頁（頁 id）：${ids.join('、')}
每頁讀：${ids.map(id => mdOf(id)).join('、')}
lint 報告：${lint}（只看你這組頁的段落，用 grep "^## <頁id> " 定位）
決策紀錄（notes）：${notes}
本輪改動：${changes}
${focus ? '特別注意：' + focus : ''}
${MD_FORMAT}
${CRITERIA}
要找的：
(a) 與 notes 矛盾（步驟、順序、結束碼、誰做、寫哪個檔）；
(b) 缺分支（判斷只有一條出路、失敗沒有終點、跨頁入口沒有對應出口）；
(c) 順序錯（例如寫檔在拿鎖之前、resolve 寫檔）；
(d) lint.md 該頁的 warn／info 候選是否成立：成立的列為 category='lint'，description 開頭寫規則代號；不成立的不用列。
只回報真正的問題；page 一律填頁 id；id 填 <id>.md 裡的 node／edge id。不要建議改設計。`,
  })),
  ...layoutGroups.map((ids, i) => ({
    kind: '排版', label: `排版 ${i + 1}/${layoutGroups.length}`, ids,
    prompt: `你是圖面排版審查員（第 ${i + 1} 組，共 ${layoutGroups.length} 組）。用 Read 工具逐一看這些 50% 縮圖（白底）：
${ids.map(id => `- ${pngOf(id) ?? '（無縮圖）'}（頁 id ${id}）`).join('\n')}
需要對照 id 時讀 ${extracted}/<頁id>.md（node 座標在同目錄的 <頁id>.json）。
本輪改動：${changes}
${focus ? '特別注意：' + focus : ''}
${CRITERIA}
只找「人眼才看得出」的問題：線標籤位置（壓線、離線太遠、貼到別的框）、可讀性（字擠、框太小、縮圖下讀不出）、線太繞或交叉、元件重疊、頁面裁切。
機械可查的（懸空、顏色、名詞表）已由 lint 處理，不要重複。只回報真正的問題；page 填頁 id；id 填元件 id 或元件上的文字。`,
  })),
  {
    kind: '其他', label: '一格一事判定', ids: pageIds,
    prompt: `你負責判定「一格一事」候選。讀 ${lint}，用 grep "\\[onething\\]" 抓出所有候選（每行含頁段落的頁 id、格子 id、分隔詞計數與全文）；
只看這些頁：${pageIds.join('、')}。
${CRITERIA}
第 7 條是你的唯一判準：一格文字裡是否有「兩個獨立動作」（例如「寫 A 並刪 B」「檢查 X 然後重生 Y」）。
以下不算兩件事：一個動作＋它的參數清單（「排除 a、b、c」）、一個動作＋失敗結束碼註記（「…（失敗 → 1 + 6-38）」）、
一個判斷結果的標籤（「否：…」）、一個動作的補充說明（括號內）。
真的兩件事才列（category='lint'，description 以「onething：」開頭並寫出建議拆成哪兩格）；必要時讀 ${extracted}/<頁id>.md 看上下文。
page 填頁 id；id 填格子 id。`,
  },
]

const VERDICT = {
  type: 'object',
  properties: { real: { type: 'boolean' }, reason: { type: 'string' } },
  required: ['real', 'reason'],
}

const verify = (f, src) => agent(`請對照抽取結果與縮圖確認這個審查意見是否成立。
頁 id：${f.page}；文字抽取：${mdOf(f.page)}（可 grep id）；縮圖：${pngOf(f.page) ?? '（無）'}；lint：${lint}
意見（來源：${src}）：[${f.page}] ${f.id}（${f.category}）：${f.description}
用 Read 看 md（排版類再看縮圖）。若確實如此 → real=true；若意見錯誤、id 不存在、或已不存在 → real=false。只判定，不擴充。`,
  { label: `驗證：${f.page} ${f.id}`, phase: '驗證', schema: VERDICT, agentType: 'general-purpose', effort: 'low' })
  .then(v => ({ ...f, source: src, real: v?.real ?? true, reason: v?.reason ?? '（驗證代理未回應，保守視為成立）' }))

const results = await pipeline(finders,
  t => agent(t.prompt, { label: t.label, phase: t.kind, schema: FINDINGS, agentType: 'general-purpose' }),
  (r, t) => {
    const fs = (r?.findings ?? []).filter(f => pageIds.includes(f.page))
    const dropped = (r?.findings ?? []).length - fs.length
    if (dropped) log(`${t.label}：${dropped} 條 page 不在白名單，略過`)
    log(`${t.label}：${fs.length} 條 → 逐條驗證`)
    return { label: t.label, verdict: r?.verdict ?? '（無）', findings: fs }
  },
  r => pipeline(r.findings, f => verify(f, r.label)).then(vs => ({ ...r, verified: vs.filter(Boolean) })),
)

// ───────────────── 彙整 ─────────────────
const done = results.filter(Boolean)
const verified = done.flatMap(r => r.verified)
const confirmed = verified.filter(f => f.real)
const rejected = verified.filter(f => !f.real)
const byPage = {}
for (const f of confirmed) (byPage[f.page] ??= []).push({ id: f.id, category: f.category, description: f.description, must_fix: f.must_fix, source: f.source })
for (const k of Object.keys(byPage)) byPage[k].sort((a, b) => (b.must_fix - a.must_fix))
const lintMechanical = Array.isArray(lint_items)
  ? lint_items.filter(i => i.level === 'warn' && (!pages?.length || pages.includes(i.page) || i.page === '跨頁'))
      .map(i => ({ page: i.page, rule: i.rule, id: i.id, msg: i.msg }))
  : { note: `未傳 args.lint_items；機械 lint 結果請直接看 ${lint}` }
log(`確認 ${confirmed.length} 條（must_fix ${confirmed.filter(f => f.must_fix).length}）、駁回 ${rejected.length} 條`)
return {
  verdicts: Object.fromEntries(done.map(r => [r.label, r.verdict])),
  confirmed: byPage,
  must_fix_count: confirmed.filter(f => f.must_fix).length,
  rejected: rejected.map(f => ({ page: f.page, id: f.id, description: f.description, reason: f.reason, source: f.source })),
  lint_mechanical: lintMechanical,
}
