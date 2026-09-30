export const meta = {
  name: 'doc-review',
  description: 'Claude 與 codex 雙軌審查文件，交叉比對後只留兩軌一致的結論',
  whenToUse: '對外契約、名詞表、不變量這類文件改完之後、定案之前',
  phases: [
    { title: 'Claude 審查', detail: 'Claude 子代理每個面向一個，只讀不改，回結構化 findings' },
    { title: 'codex 審查', detail: '每個面向跑一次 codex exec，子代理把輸出轉成同一個 schema' },
    { title: '交叉比對', detail: '一個代理讀檔查證，只把雙方一致的當結論，站不住腳的駁回' },
  ],
}

// args 契約：
//   repo?        string   預設 '/home/cyc/Desktop/vendor-kit_ws/src'
//   round        string   必填，用來命名 codex 的輸出檔（例如 'r87'）
//   background?  string   已定案的前提（會明寫「不要質疑」）
//   angles       array    必填，每項 { key, label, ask }
//   tracks?      array    預設 ['claude', 'codex']
//   cross_check? boolean  預設 true
//   effort?      object   { review, cross }
const {
  repo = '/home/cyc/Desktop/vendor-kit_ws/src',
  round,
  background = '',
  angles,
  tracks = ['claude', 'codex'],
  cross_check = true,
  effort = {},
} = args ?? {}

// ───────────────── 參數檢查 ─────────────────
if (typeof round !== 'string' || !round.trim()) {
  throw new Error('args.round 是必填字串（codex 輸出檔名用，例如 "r87"）；目前沒給或不是字串')
}
if (!Array.isArray(angles) || angles.length === 0) {
  throw new Error('args.angles 是必填陣列，每項要有 { key, label, ask }；目前沒給或是空陣列')
}
const badAngles = angles
  .map((a, i) => ({ i, a }))
  .filter(({ a }) => !a || typeof a.key !== 'string' || !a.key || typeof a.label !== 'string' || !a.label || typeof a.ask !== 'string' || !a.ask)
if (badAngles.length) {
  throw new Error(`args.angles 第 ${badAngles.map(x => x.i).join('、')} 項缺欄位：每項都要有非空的 key、label、ask`)
}

const VALID_TRACKS = ['claude', 'codex']
const useTracks = VALID_TRACKS.filter(t => (Array.isArray(tracks) ? tracks : []).includes(t))
if (!useTracks.length) {
  throw new Error(`args.tracks 過濾後是空的：只接受 ${VALID_TRACKS.join('、')}，目前給的是 ${JSON.stringify(tracks)}`)
}

const codexOut = key => `${repo}/doc/decisions/review_log/codex/${round}-${key}.md`

// ───────────────── 共用護欄（要組進每個子代理的 prompt，不只寫註解） ─────────────────
const GUARDRAILS = `硬性規則（違反就算這輪失敗）：
1. 不 commit、不 push、不跑任何 git 寫入指令（含 add、checkout、reset、stash、tag）。
2. 會改檔的話，改前先備份到 ${repo}/doc/decisions/_backup/，命名 <路徑攤平>.pre_${round}.<ext>（例如 agents_domain.pre_${round}.md）；同名已存在就在副檔名前加序號。
3. 不准動 ${repo}/doc/decisions/_backup/、doc/decisions/review_log/、doc/decisions/_marked/（歷史快照與本地產物），除非這個 task 明說。
4. 驗證一律用腳本／grep／wc 算出來，不要目視判斷「看起來對」。`

const BACKGROUND = background && background.trim()
  ? `背景（已定案，不要質疑、不要重新設計）：\n${background.trim()}`
  : '（沒有給額外背景前提。）'

// ───────────────── 兩軌共用的 findings schema ─────────────────
const ITEM = {
  type: 'object',
  properties: {
    where: { type: 'string', description: '檔案路徑＋位置（行號、標題或錨點）' },
    what: { type: 'string', description: '問題是什麼，一句話' },
    why: { type: 'string', description: '為什麼是問題／建議怎麼改，一句話' },
  },
  required: ['where', 'what', 'why'],
}
const REVIEW = {
  type: 'object',
  properties: {
    angle: { type: 'string', description: '面向的 key' },
    must_fix: { type: 'array', items: ITEM, description: '事實錯誤、壞連結、結構破損、與定案衝突' },
    suggest: { type: 'array', items: ITEM, description: '措辭、一致性、可讀性' },
    ok: { type: 'array', items: { type: 'string' }, description: '查過沒問題的項目，一行一條' },
    error: { type: 'string', description: '這一軌失敗的原因；成功就留空。失敗時 must_fix 要是空陣列，不要編內容' },
  },
  required: ['angle', 'must_fix', 'suggest', 'ok'],
}

// ───────────────── Claude 軌：只讀，多面向平行 ─────────────────
const claudeTrack = () => parallel(angles.map(angle => () =>
  agent(`你是文件審查員。**只讀，不要改任何檔**（這一軌純審查，一個字都不要動）。

${GUARDRAILS}

${BACKGROUND}

審查面向：${angle.label}

${angle.ask}

回報方式：分 must_fix（必改）、suggest（建議）、ok（查過沒問題）。每條寫清楚位置（檔案＋行號或標題）、問題、一句建議。
用繁體中文、白話、不要客套話。查不到證據的就不要寫進 must_fix。angle 欄位填 "${angle.key}"。`,
    {
      label: `Claude：${angle.label}`,
      phase: 'Claude 審查',
      schema: REVIEW,
      agentType: 'general-purpose',
      ...(effort.review ? { effort: effort.review } : {}),
    })
))

// ───────────────── codex 軌：子代理負責啟動 codex，再把輸出轉成同一個 schema ─────────────────
const codexBrief = angle => `只讀，不要改任何檔。

${BACKGROUND}

主題：${angle.label}

${angle.ask}

輸出 markdown，分「必改」「建議」「沒問題」三區，每條寫位置（檔案＋行號或標題）＋一句建議。不要客套話。`

const codexTrack = () => parallel(angles.map(angle => () =>
  agent(`你的工作是啟動 codex 做獨立審查，然後把 codex 的輸出整理成結構化回報。**不要自己審、不要改檔、不要加入你自己的意見。**

${GUARDRAILS}

步驟：
1. 先確保輸出目錄存在：\`mkdir -p ${repo}/doc/decisions/review_log/codex\`
2. 把下面「brief」那段用 heredoc 寫進暫存檔（放你的 scratchpad），或直接當引號參數傳給 codex；不要讓 shell 的引號吃掉內容。
3. 前景執行（Bash timeout 600000，不要 run_in_background），指令形狀一字不差：

codex exec --skip-git-repo-check -C ${repo} -o ${codexOut(angle.key)} "<brief>" < /dev/null

   - **\`< /dev/null\` 不可省略**：省了 codex 會停在等 stdin，整條 workflow 會卡死。
   - **不要帶 --sandbox**：這個 repo 的 .codex/config.toml 已經設 danger-full-access。
   - 輸出檔固定 ${codexOut(angle.key)}。
4. codex 跑完後讀 ${codexOut(angle.key)}，把「必改」放進 must_fix、「建議」放進 suggest、「沒問題」放進 ok，每條保留位置＋問題＋一句建議。
5. codex 失敗、逾時或輸出是空的：must_fix／suggest／ok 都回空陣列，並在 error 欄位寫失敗原因（含你看到的錯誤訊息）。**不要假裝有結果、不要自己補內容。**

angle 欄位填 "${angle.key}"。回報用繁體中文。

brief（餵給 codex 的內容）：
${codexBrief(angle)}`,
    {
      label: `codex：${angle.label}`,
      phase: 'codex 審查',
      schema: REVIEW,
      agentType: 'general-purpose',
      ...(effort.review ? { effort: effort.review } : {}),
    })
))

// 兩軌同時開始：把兩軌各自包成一個 thunk 一起丟進 parallel，
// 不要「先跑完 Claude 再跑 codex」。phase 由 opts.phase 明寫，不靠全域 phase() 狀態（會 race）。
log(`${round}：${useTracks.join(' + ')} 雙軌審查，${angles.length} 個面向（${angles.map(a => a.key).join('、')}）`)
const trackResults = await parallel(useTracks.map(t => (t === 'claude' ? claudeTrack : codexTrack)))
const byTrack = {}
useTracks.forEach((t, i) => { byTrack[t] = (trackResults[i] ?? []).filter(Boolean) })
const claudeResults = byTrack.claude ?? null
const codexResults = byTrack.codex ?? null

const count = rs => (rs ?? []).reduce((n, r) => n + (r.must_fix?.length ?? 0), 0)
log(`Claude 軌 must_fix ${count(claudeResults)} 條、codex 軌 must_fix ${count(codexResults)} 條`)

// ───────────────── 交叉比對：只有兩軌都跑了才有意義 ─────────────────
const CROSS = {
  type: 'object',
  properties: {
    agreed: {
      type: 'array',
      description: '兩軌都指出、且你查證成立的：措辭合併成一條，並標出兩邊各自寫的位置',
      items: {
        type: 'object',
        properties: {
          what: { type: 'string', description: '合併後的問題敘述' },
          where: { type: 'string', description: '你查證後確認的位置' },
          fix: { type: 'string', description: '建議改法，一句話' },
          claude_where: { type: 'string', description: 'Claude 軌寫的位置' },
          codex_where: { type: 'string', description: 'codex 軌寫的位置' },
        },
        required: ['what', 'where', 'fix', 'claude_where', 'codex_where'],
      },
    },
    claude_only: { type: 'array', items: ITEM, description: '只有 Claude 軌提出、你查證成立的' },
    codex_only: { type: 'array', items: ITEM, description: '只有 codex 軌提出、你查證成立的' },
    rejected: {
      type: 'array',
      description: '你判定站不住腳的（不管哪一軌提的）',
      items: {
        type: 'object',
        properties: {
          from: { type: 'string', description: 'claude／codex／both' },
          what: { type: 'string', description: '被駁回的說法' },
          why_rejected: { type: 'string', description: '為什麼駁回：你查到的實際情形' },
        },
        required: ['from', 'what', 'why_rejected'],
      },
    },
  },
  required: ['agreed', 'claude_only', 'codex_only', 'rejected'],
}

let cross = null
if (cross_check && claudeResults && codexResults) {
  // 兩軌都收完才跑，這時全域 phase() 不會 race
  phase('交叉比對')
  cross = await agent(`兩軌對同一批文件的獨立審查結果如下（JSON）。你的工作是交叉比對。

${GUARDRAILS}

這一階段也是**只讀**：不要改任何檔。

Claude 軌：
${JSON.stringify(claudeResults, null, 2)}

codex 軌：
${JSON.stringify(codexResults, null, 2)}

${BACKGROUND}

做法：
1. **不要照單全收任一軌**：每一條都自己去 ${repo} 讀檔查證（行號、連結、字串出現次數都用 grep／腳本算，不要目視）。
2. agreed：兩軌都指出、而且你查證成立的。措辭合併成一條，並標出兩邊各自寫的位置（可能同一件事位置寫得不一樣）。
3. claude_only／codex_only：只有一軌提出、但你查證成立的。
4. rejected：你判定站不住腳的（看錯、過度推論、與已定案背景衝突），每條寫為什麼駁回，附你查到的實際情形。
5. 每條都要有位置。查不到證據的一律進 rejected，不要放進 agreed。

繁體中文，白話，不要重寫文件內容。`,
    {
      label: '交叉比對',
      phase: '交叉比對',
      schema: CROSS,
      agentType: 'general-purpose',
      ...(effort.cross ? { effort: effort.cross } : {}),
    })
  log(`交叉比對：一致 ${cross?.agreed?.length ?? 0} 條、駁回 ${cross?.rejected?.length ?? 0} 條`)
} else if (cross_check) {
  log('只跑了單軌，跳過交叉比對（沒有第二軌可以比）')
}

return { round, tracks: useTracks, claude: claudeResults, codex: codexResults, cross }

// ───────────────── 最小 args 範例（JSON） ─────────────────
// {
//   "round": "r87",
//   "background": "審閱頁只有兩頁：01_purpose.md（目的與承諾）、02_invariants.md（不變量）；名詞全在根 GLOSSARY.md。",
//   "angles": [
//     {
//       "key": "terms",
//       "label": "GLOSSARY.md 名詞完整性",
//       "ask": "審 GLOSSARY.md：定義是否一兩句、有沒有寫進規則或實作細節、目錄錨點是否都解得開（自己算 slug 比對）。"
//     },
//     {
//       "key": "consistency",
//       "label": "01 與 02 的一致性",
//       "ask": "審 docs/contract/01_purpose.md 與 02_invariants.md：01 每條承諾在 02 是否有對應性質；兩頁有沒有用 GLOSSARY.md 沒定義的詞。"
//     }
//   ]
// }
