export const meta = {
  name: 'diagram-page',
  description: '畫一頁流程圖或架構圖：子代理照規格用 drawio MCP 逐格畫、匯出自查版面，再交給 codex 只讀審查；全程禁止 git 寫入',
  whenToUse: '要新畫或重畫 proposal_claude_v3.drawio 的某一頁時；主對話不自己畫',
  phases: [
    { title: '繪製', detail: '一個子代理照 spec 用 edit_diagram 逐格畫，匯出 PNG 自查壓線與重疊，存回 .drawio' },
    { title: 'codex 審查', detail: '子代理啟動 codex（附圖、只讀）對照契約審這一頁，把輸出整理成必改／建議／不同做法' },
  ],
}

// args 契約：
//   repo?        string  預設 '/home/cyc/Desktop/vendor-kit_ws/src'
//   page_id      string  必填，圖的持久鍵 <diagram id>，例如 'c-dev'
//   page_name    string  必填，頁名（標題就寫在頁名）
//   what         string  必填，這頁畫什麼，一句話（給 codex 看）
//   spec         string  必填，版面規格：泳道、每一格（文字、類型、位置）、每條線（起訖、標籤）
//   settled?     string  已定的規則（codex 不要建議推翻），會附在固定規則之後
//   read_first?  string[] codex 要先讀的契約檔（預設 01、02、CONTEXT.md、STYLE.md、doc/adr/）
//   drawio_file? string  預設 'doc/decisions/research/diagram_proposals/proposal_claude_v3.drawio'
//   effort?      object  { draw, review }
const {
  repo = '/home/cyc/Desktop/vendor-kit_ws/src',
  page_id,
  page_name,
  what,
  spec,
  settled = '',
  read_first = [
    'doc/decisions/review/01_purpose.md',
    'doc/decisions/review/02_invariants.md',
    'CONTEXT.md',
    'script/diagram/STYLE.md',
    'doc/adr/（全部）',
  ],
  drawio_file = 'doc/decisions/research/diagram_proposals/proposal_claude_v3.drawio',
  effort = {},
} = args ?? {}

// ───────────────── 參數檢查 ─────────────────
const missing = ['page_id', 'page_name', 'what', 'spec'].filter(k => typeof ({ page_id, page_name, what, spec })[k] !== 'string' || !({ page_id, page_name, what, spec })[k].trim())
if (missing.length) {
  throw new Error(`args 缺必填字串：${missing.join('、')}。page_id 是 <diagram id>、page_name 是頁名、what 是一句話說這頁畫什麼、spec 是完整版面規格`)
}

const LOG_DIR = `${repo}/doc/decisions/review_log/diagram`
const PNG = `${LOG_DIR}/page_${page_id}.png`
const BRIEF = `${LOG_DIR}/brief_codex_${page_id}.md`
const CODEX_OUT = `${LOG_DIR}/codex_${page_id}.md`

// ───────────────── 共用護欄（組進每個子代理的 prompt） ─────────────────
const GUARDRAILS = `硬性規則（違反就算這輪失敗）：
1. 不 commit、不 push、不跑任何 git 寫入指令（含 add、checkout、reset、stash）。唯讀的 git status／diff 可以。
2. 圖只准用 drawio MCP 的 edit_diagram 逐格 add／update／delete。禁止 load_diagram、create_new_diagram、禁止用腳本產生整份 XML 再載入——那會蓋掉其他頁。
3. 只動頁 id「${page_id}」。其他頁一格都不要碰。
4. 驗證用匯出的 PNG 實際看、或用 get_diagram 算座標，不要憑印象說「應該沒壓線」。`

const DRAW_RULES = `圖面規則（照 ${repo}/script/diagram/STYLE.md。流程頁以第 7 節為準，它優先於前面各節講流程頁的部分；架構頁看第 6 節）：
- 標題寫在頁名，頁面上不放標題格；格子只寫名字或動作，不寫括號說明、不粗體。
- 流程頁不分泳道、不上顏色、不用紅框：判斷是白底菱形（rhombus;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontSize=14），起點／終點是白底橢圓（ellipse，同樣 strokeWidth=2），步驟是白底圓角方塊（rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=1;fontSize=14）。
- 誰做的用底色分，不用泳道，流程排法不因此改變：使用者做的步驟 fillColor=#FFF4C3、主機做的步驟 fillColor=#f5f5f5、引擎做的步驟白色；判斷、起點、終點一律白色。
- 要標區塊就畫有名字的虛線框（rounded=1;dashed=1;fillColor=none;strokeColor=#666666;verticalAlign=top;align=left;spacingLeft=8;fontSize=14;），parent="1"，先 add 虛線框再 add 格子，讓框在下層。框的標題不得壓到框內格子或線。
- 使用者視角：只畫使用者看得到的判斷與結果，不展開執行紀錄、進度檔、預檢、取件細節。
- 線：edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;endFill=1;strokeWidth=2;fontSize=14。水平線的是／否標籤 verticalAlign=bottom，垂直線的標籤 align=left;spacingLeft=6。
- 文字不得壓線、不得壓虛線框邊；標籤太靠近邊時用 mxGeometry x（-0.5～-0.9）往起點移。
- 線交叉不可避免時用 jumpStyle=arc;jumpSize=12。
- 版面緊湊，不留大片空白。
- 圖例放在最下方：菱形「判斷」、橢圓「起點／終點」、圓角方塊「步驟」、虛線框「區塊」、淡黃步驟「使用者做的」、淺灰步驟「主機做的」（有出現才放），外加文字「數字 = 退出碼；實線 = 執行順序」。
- HTML 值要雙重跳脫，例如 &amp;lt;ns&amp;gt;。`

// ───────────────── 繪製 ─────────────────
const DRAW = {
  type: 'object',
  properties: {
    png: { type: 'string', description: '最後一次匯出、確認過的 PNG 絕對路徑' },
    cells: { type: 'number', description: '這頁最後的 cell 數' },
    deviations: { type: 'array', items: { type: 'string' }, description: '跟 spec 不同的地方與理由；沒有就空陣列' },
    checked: { type: 'array', items: { type: 'string' }, description: '自查過的項目與結果，一行一條' },
    error: { type: 'string', description: '失敗原因；成功留空' },
  },
  required: ['png', 'cells', 'deviations', 'checked'],
}

phase('繪製')
const drawn = await agent(`你負責畫 ${drawio_file} 的一頁：頁 id「${page_id}」，頁名「${page_name}」。

${GUARDRAILS}

${DRAW_RULES}

步驟：
1. 用 ToolSearch 載入 mcp__drawio__list_pages、get_diagram、edit_diagram、rename_page、add_page、export_diagram。
2. list_pages。頁不存在就 add_page（id="${page_id}"、name="${page_name}"）；存在但頁名不同就 rename_page。
3. get_diagram 這一頁（edit_diagram 之前必做）。頁上有舊內容就逐一 delete。
4. 照下面的 spec 用 edit_diagram 逐格 add：先泳道，再格子（parent 設成所屬泳道，座標相對泳道），再線（parent="1"）。一次呼叫可以放多個 operation。
5. export_diagram 這一頁成 PNG 到 ${PNG}。**匯出後檢查檔案大小**：小於 150KB 多半是壞檔（瀏覽器還沒渲染完），重匯一次；用 Read 看圖。
6. 逐項自查：文字壓線、文字壓泳道邊界、格子重疊、線穿過格子、懸空的線、每個判斷的出口都有標籤。有問題就 update 修，再匯出再看，直到乾淨。
7. 最後 export_diagram（不帶 page_id）整份存回 ${repo}/${drawio_file}。
8. 回報：PNG 路徑、cell 數、跟 spec 不同的地方（理由）、自查結果。失敗就寫 error，不要假裝完成。

spec：
${spec}`,
  {
    label: `繪製：${page_name}`,
    phase: '繪製',
    schema: DRAW,
    agentType: 'general-purpose',
    ...(effort.draw ? { effort: effort.draw } : {}),
  })

if (!drawn || drawn.error) {
  log(`繪製失敗：${drawn?.error ?? '子代理沒有回傳'}；不送 codex 審查`)
  return { page_id, drawn, review: null }
}
log(`繪製完成：${drawn.cells} 格，${drawn.deviations.length} 處跟 spec 不同`)

// ───────────────── codex 審查 ─────────────────
const briefText = `你是圖面審查者。**只讀、不要改任何檔**。我要的是你**不同的建議**，不是替圖背書。

附圖是 vendor_kit（VK）「${page_name}」頁的匯出圖。原始檔是 \`${drawio_file}\` 的頁 id \`${page_id}\`。它畫的是：${what}

## 先讀的東西（圖要對齊它們）
${read_first.map(f => `- \`${f}\``).join('\n')}

## 已經定下的規則（不要再建議推翻它們）
- 標題寫在頁名，頁面上不放標題
- 流程頁不分泳道、不用紅框（STYLE §7）：菱形 = 判斷、橢圓 = 起點／終點、圓角方塊 = 步驟、虛線框 = 區塊；終點裡的數字 = 退出碼。唯一的顏色是誰做的：淡黃 = 使用者、淺灰 = 主機、白 = 引擎。不要建議加泳道或別的配色
- 層級 = 使用者視角：執行紀錄、進度檔、預檢、退出碼 3、取件細節、要改先問的 -y／CI 規則另開共用頁，不要因為沒畫它們而列為缺漏
- 文字不壓線、不壓框邊；版面要緊湊
${settled.trim() ? settled.trim() : ''}

## 請回答
1. **正確性**：每個判斷、分支、順序、退出碼、步驟所在的泳道，跟契約有沒有對不上的地方？逐條列，附出處（檔名＋條號或節號）。
2. **缺漏**：這個流程中契約規定、使用者看得到、但圖上沒畫的判斷或結果？
3. **多餘**：不該出現在這一頁的東西？
4. **可讀性**：第一次看的人哪裡會看不懂或誤讀？指出是哪一格或哪一條線。
5. **你會怎麼畫得不一樣**：每一條寫理由，並說明跟上面已定的規則有沒有衝突。

輸出 markdown。每一條寫：位置、問題、建議、理由。分「必改（跟契約衝突）」「建議」「只是不同做法」三類。不要客套話。`

const ITEM = {
  type: 'object',
  properties: {
    where: { type: 'string', description: '圖上哪一格或哪一條線' },
    what: { type: 'string', description: '問題，一句話' },
    fix: { type: 'string', description: '建議改法，一句話' },
    source: { type: 'string', description: 'codex 引的契約出處；沒有就空字串' },
  },
  required: ['where', 'what', 'fix', 'source'],
}
const REVIEW = {
  type: 'object',
  properties: {
    output_file: { type: 'string' },
    must_fix: { type: 'array', items: ITEM },
    suggest: { type: 'array', items: ITEM },
    different: { type: 'array', items: ITEM, description: '「只是不同做法」' },
    error: { type: 'string', description: 'codex 失敗的原因；成功留空。失敗時三個陣列都要是空的，不要編內容' },
  },
  required: ['output_file', 'must_fix', 'suggest', 'different'],
}

const review = await agent(`你的工作是啟動 codex 審一頁圖，然後把 codex 的輸出整理成結構化回報。**不要自己審、不要改圖、不要加入你自己的意見。**

${GUARDRAILS}

步驟：
1. 確認圖檔存在：${drawn.png}。不是 ${PNG} 的話先 cp 過去。
2. 把下面「brief」原文用 heredoc（引號包住的 'EOF'）寫進 ${BRIEF}。
3. 前景執行（Bash timeout 600000，不要 run_in_background），指令形狀一字不差：

codex exec --skip-git-repo-check -C ${repo} -i ${PNG} -o ${CODEX_OUT} "$(cat ${BRIEF})" < /dev/null

   - **\`< /dev/null\` 不可省略**：省了 codex 會停在等 stdin，整條 workflow 會卡死。
   - **不要帶 --sandbox**：repo 的 .codex/config.toml 已設 danger-full-access。
4. 讀 ${CODEX_OUT}，把「必改」放 must_fix、「建議」放 suggest、「只是不同做法」放 different，每條保留位置、問題、建議、出處。output_file 填 ${CODEX_OUT}。
5. codex 失敗、逾時或輸出是空的：三個陣列都回空，error 寫原因與錯誤訊息。**不要假裝有結果。**

回報用繁體中文。

brief：
${briefText}`,
  {
    label: `codex 審查：${page_name}`,
    phase: 'codex 審查',
    schema: REVIEW,
    agentType: 'general-purpose',
    ...(effort.review ? { effort: effort.review } : {}),
  })

if (review && !review.error) {
  log(`codex：必改 ${review.must_fix.length}、建議 ${review.suggest.length}、不同做法 ${review.different.length}`)
} else {
  log(`codex 審查失敗：${review?.error ?? '子代理沒有回傳'}`)
}
return { page_id, drawn, review }

// ───────────────── args 範例（可直接貼進 Workflow 的 args） ─────────────────
// {
//   "page_id": "c-dev",
//   "page_name": "dev 流程",
//   "what": "使用者 just vendor_kit dev 讓工具或引擎改用本機開發來源的流程",
//   "spec": "泳道：使用者 x20 y40 w200；引擎 x240 y40 w480。格子：……線：……",
//   "settled": "- dev 只寫不進 git 的檔（version.local.toml、cache/）"
// }
