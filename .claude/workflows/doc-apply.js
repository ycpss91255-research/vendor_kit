export const meta = {
  name: 'doc-apply',
  description: '分組並行套用文件改動並驗證：每組一個子代理改檔，改前備份，驗證一律用腳本算，全程禁止 git 寫入',
  whenToUse: '一輪審查定案後要動多個檔時；單一檔的小改不用（直接改就好）',
  phases: [
    { title: '修正', detail: '每個 task 一個子代理並行改檔，帶共用護欄與背景，回報改了什麼與備份路徑' },
    { title: '驗證', detail: '並行跑驗證組（預設：壞連結、舊說法殘留、宣稱 vs git diff 落差），只讀不改' },
  ],
}

// args: {
//   repo?: string,        // 預設 '/home/cyc/Desktop/vendor-kit_ws/src'
//   round: string,        // 必填，備份後綴，例如 'r87' → *.pre_r87.md
//   background?: string,  // 共用背景：已定案的事實、改名史、不要重做的事
//   tasks: { key, label, ask, files? }[],   // 必填，每項一個並行子代理；files 是範圍提示
//   verify?: { key, label, ask }[],         // 沒給就用內建預設三組；給空陣列 = 跳過驗證
//   effort?: { apply?: string, verify?: string },  // 'low'|'medium'|'high'|'xhigh'|'max'
// }
const {
  repo = '/home/cyc/Desktop/vendor-kit_ws/src',
  round,
  background,
  tasks,
  verify,
  effort,
} = args ?? {}

// ───────────────── 參數檢查（缺什麼講清楚，不要讓子代理跑一半才發現） ─────────────────
if (typeof round !== 'string' || !round.trim()) {
  throw new Error('args.round 必填：備份檔名後綴用的輪次字串，例如 "r87"（會產生 <路徑攤平>.pre_r87.md）')
}
if (!Array.isArray(tasks) || tasks.length === 0) {
  throw new Error('args.tasks 必填：至少一項 { key, label, ask, files? }；每項會開一個並行子代理改檔')
}
const badTasks = tasks
  .map((t, i) => ({ i, miss: ['key', 'label', 'ask'].filter(k => typeof t?.[k] !== 'string' || !t[k].trim()) }))
  .filter(x => x.miss.length)
if (badTasks.length) {
  throw new Error(`args.tasks 有項目缺欄位：${badTasks.map(x => `第 ${x.i + 1} 項缺 ${x.miss.join('、')}`).join('；')}`)
}
// verify 的型別先擋掉，不要等修正跑完才炸
if (verify != null && !Array.isArray(verify)) {
  throw new Error('args.verify 要是陣列（每項 { key, label, ask }），或整個不給以使用內建預設驗證組；給空陣列 = 跳過驗證')
}

const applyEffort = effort?.apply          // 不給就繼承 session
const verifyEffort = effort?.verify ?? 'low'   // 驗證是機械活，預設便宜跑

// ───────────────── 共用護欄：組進每個子代理的 prompt，不是只寫在註解 ─────────────────
const NO_TOUCH = 'doc/decisions/_backup/、doc/decisions/review_log/、doc/decisions/_marked/'

const GUARD_WRITE = `Repo ${repo}。以下是硬性護欄，違反就算這個 task 失敗：

1. **不 commit、不 push、不跑任何 git 寫入指令**（commit／push／add／reset／checkout／stash／rebase／tag 一概不准）。只讀的 git status／git diff 可以。
2. 會改檔的話，**改前先備份**到 ${repo}/doc/decisions/_backup/，命名 <路徑攤平>.pre_${round}.<ext>（把路徑的 / 換成 _，例如 docs/agents/domain.md → agents_domain.pre_${round}.md）；同名已存在就在後綴加序號（…pre_${round}.2.md）。回報實際的備份檔路徑。
3. **不准動** ${NO_TOUCH}（歷史快照與本地產物），除非這個 task 的指示明說可以動哪個檔。
4. **驗證一律用腳本／grep 算，不要目視**：改完自己 grep 一次確認，回報的數字要是跑出來的。`

const GUARD_READ = `Repo ${repo}。以下是硬性護欄：

1. **只讀與驗證，不要改任何檔**；**不 commit、不 push、不跑任何 git 寫入指令**。只讀的 git status／git diff 可以。
2. 掃描範圍**排除** ${NO_TOUCH}（歷史快照與本地產物）。
3. **驗證一律用腳本／grep 算，不要目視**：回報的數字要是跑出來的。
4. 發現問題只回報，不要自己修。`

const BACKGROUND_BLOCK = typeof background === 'string' && background.trim()
  ? `\n共用背景（已定案的事實／改名史／不要重做的事）：\n${background}\n`
  : ''

const filesBlock = t => (Array.isArray(t.files) && t.files.length
  ? `\n這一輪你只准動這些檔：${t.files.join('、')}\n（其他檔即使看到問題也只回報，不要改。）\n`
  : '')

// ───────────────── schema ─────────────────
const APPLY_SCHEMA = {
  type: 'object',
  properties: {
    key: { type: 'string', description: '這個 task 的 key，原樣填回' },
    changed: {
      type: 'array',
      description: '實際改到的檔',
      items: {
        type: 'object',
        properties: {
          file: { type: 'string', description: 'repo 相對路徑' },
          count: { type: 'integer', description: '改了幾處' },
          summary: { type: 'string', description: '改了什麼（原文 → 新文，或一句話摘要）' },
        },
        required: ['file', 'count', 'summary'],
      },
    },
    unresolved: {
      type: 'array',
      description: '要求的事項裡沒改成的（含判斷不該改而保留的）',
      items: {
        type: 'object',
        properties: {
          what: { type: 'string', description: '哪一項沒改成' },
          why: { type: 'string', description: '原因／你的判斷' },
        },
        required: ['what', 'why'],
      },
    },
    backups: { type: 'array', description: '備份檔路徑', items: { type: 'string' } },
    checks: { type: 'string', description: '你跑了哪些 grep／腳本，結果是什麼' },
  },
  required: ['key', 'changed', 'unresolved', 'backups'],
}

const VERIFY_SCHEMA = {
  type: 'object',
  properties: {
    key: { type: 'string', description: '這個驗證組的 key，原樣填回' },
    pass: { type: 'boolean', description: '完全沒問題才 true' },
    issues: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          where: { type: 'string', description: '檔案:行號，或掃描目標' },
          what: { type: 'string', description: '問題是什麼' },
        },
        required: ['where', 'what'],
      },
    },
    detail: { type: 'string', description: '跑了什麼指令、具體數字' },
  },
  required: ['key', 'pass', 'issues'],
}

// ───────────────── 修正：每個 task 一個子代理並行 ─────────────────
phase('修正')
log(`輪次 ${round}：${tasks.length} 組並行修正（備份後綴 .pre_${round}）`)

const applyOpts = t => {
  const o = { label: t.label, phase: '修正', schema: APPLY_SCHEMA, agentType: 'general-purpose' }
  if (applyEffort) o.effort = applyEffort
  return o
}

const applied = (await parallel(tasks.map(t => () => agent(
  `${GUARD_WRITE}
${BACKGROUND_BLOCK}${filesBlock(t)}
你這一組的 key 是 \`${t.key}\`（回報時原樣填回）。任務：

${t.ask}

回報：改了哪些檔、每檔改了幾處與內容摘要、有哪些沒改成（含原因與你的判斷）、備份檔路徑、你跑的驗證指令與結果。`,
  applyOpts(t),
)))).filter(Boolean)

const changedFiles = [...new Set(applied.flatMap(r => (r.changed ?? []).map(c => c.file)))]
log(`修正完成：${applied.length}/${tasks.length} 組回報，動到 ${changedFiles.length} 個檔`)

// ───────────────── 驗證：沒給 verify 就用內建預設三組 ─────────────────
const CLAIMS = JSON.stringify(applied.map(r => ({
  key: r.key,
  changed: (r.changed ?? []).map(c => ({ file: c.file, count: c.count, summary: c.summary })),
})))

const DEFAULT_VERIFY = [
  {
    key: 'links',
    label: '驗證：壞連結',
    ask: `掃現行 md 檔的相對路徑連結與錨點是否解得開。

1. 用腳本抓出所有 .md 的 markdown 連結（含 \`[文字](路徑)\` 與 \`[文字](路徑#錨點)\`），排除 http(s) 外部連結。
2. 路徑部分：從該連結所在檔的目錄解析，確認目標檔存在。
3. 錨點部分：確認目標檔裡有對應的標題（GitHub 錨點規則：標題轉小寫、空白換 -、去掉標點）。
4. 順手檢查這一輪動到的檔有沒有被別的檔用舊路徑引用（動到的檔：${changedFiles.length ? changedFiles.join('、') : '（無）'}）。

每個壞連結的 where 填「檔案:行號」，what 寫「指向 X，X 不存在／錨點解不開」。也回報你檢查了幾個連結。`,
  },
  {
    key: 'residue',
    label: '驗證：舊說法殘留',
    ask: `抓舊說法殘留：把共用背景裡提到的 _Avoid_ 詞與舊路徑全部掃一遍，回報出現位置。

共用背景（要從裡面自己抽出「不該再出現的詞」與「已作廢的路徑／檔名」清單）：
${background && background.trim() ? background : '（這一輪沒給背景。改用 repo 根 GLOSSARY.md 的 _Avoid_ 行當清單：每個 **名詞** 條目的 _Avoid_ 詞都不該出現在現行檔的正文。）'}

做法：
1. 先列出你要掃的詞與路徑清單（回報在 detail 裡）。
2. 用 grep -rn 掃現行 md（排除護欄列的目錄）。
3. **_Avoid_ 行本身、以及明確在描述歷史／已歸檔內容的句子不算殘留**，要在 what 裡註明你怎麼判斷的。

每筆 where 填「檔案:行號」，what 寫「殘留詞／舊路徑 → 應改成什麼」。`,
  },
  {
    key: 'gap',
    label: '驗證：宣稱 vs 實際落差',
    ask: `比對修正組宣稱改了什麼 vs git diff 實際改了什麼。**只准跑唯讀的 \`git status\` 與 \`git diff\`**（可用 --stat、-U0、-- <path>），不准跑任何 git 寫入指令。

修正組的宣稱（JSON）：
${CLAIMS}

做法：
1. \`git status --porcelain\` 與 \`git diff --stat\` 取實際動到的檔（注意：這個 repo 本來就有未 commit 的既存改動，只針對上面宣稱的檔與內容比對，不要把既存改動當成問題）。
2. 逐條比對：
   - 宣稱有改、但 diff 看不到（或行數明顯不符）→ 一筆 issue，where 填檔案，what 寫「宣稱 X 處（key=…），diff 實際 0 處／N 處」。
   - diff 有改、但沒有任何 task 宣稱→ 一筆 issue，what 寫「diff 有改動但無人宣稱」，並說明看起來是這一輪造成的還是既存改動。
3. 備份檔（doc/decisions/_backup/）是預期產物，不算「無人宣稱」，但要確認每個宣稱改過的檔都有對應備份；沒有的列為 issue。

pass 只在沒有任何落差時為 true。`,
  },
]

let verified = []
const verifySpecs = verify == null ? DEFAULT_VERIFY : verify

if (verifySpecs.length === 0) {
  log('args.verify 給了空陣列：跳過驗證階段')
} else {
  phase('驗證')
  log(`${verifySpecs.length} 組並行驗證（effort ${verifyEffort}）${verify == null ? '：內建預設組' : ''}`)
  verified = (await parallel(verifySpecs.map((v, i) => () => agent(
    `${GUARD_READ}

剛套用一輪文件改動（輪次 ${round}，${tasks.length} 組修正，動到：${changedFiles.length ? changedFiles.join('、') : '（回報中沒有改到檔）'}）。
你這一組的 key 是 \`${v.key ?? `verify_${i + 1}`}\`（回報時原樣填回）。要驗的是：

${v.ask}`,
    { label: v.label ?? `驗證 ${i + 1}`, phase: '驗證', schema: VERIFY_SCHEMA, agentType: 'general-purpose', effort: verifyEffort },
  )))).filter(Boolean)
}

// ───────────────── 彙整：unresolved 給主對話直接轉述 ─────────────────
const unresolved = [
  ...applied.flatMap(r => (r.unresolved ?? []).map(u => ({
    from: `修正／${r.key}`,
    what: u.what,
    why: u.why,
  }))),
  ...verified.filter(v => !v.pass).flatMap(v => (v.issues ?? []).map(i => ({
    from: `驗證／${v.key}`,
    what: `${i.where}：${i.what}`,
    why: v.detail ?? '',
  }))),
]

log(`完成：修正 ${applied.length} 組、驗證 ${verified.length} 組（未通過 ${verified.filter(v => !v.pass).length}）、待處理 ${unresolved.length} 條`)

return { round, applied, verified, unresolved }

// ───────────────── args 範例（可直接貼進 Workflow 的 args） ─────────────────
// {
//   "round": "r87",
//   "background": "已定案的改名：專案→repo、動詞→recipe。這些 _Avoid_ 詞不得出現在現行檔正文（_Avoid_ 行本身除外）。名詞表是根 GLOSSARY.md，審閱頁只剩 docs/contract/01_purpose.md 與 docs/contract/02_invariants.md。",
//   "tasks": [
//     {
//       "key": "purpose",
//       "label": "01_purpose.md",
//       "ask": "改 docs/contract/01_purpose.md：1. 全檔掃 _Avoid_ 詞，有殘留就改。2. 第 3 行指向名詞表的相對路徑改指根 GLOSSARY.md（驗證過可解再寫）。回報改了哪幾行與掃描結果。",
//       "files": ["docs/contract/01_purpose.md"]
//     },
//     {
//       "key": "adr",
//       "label": "docs/adr/（README、TEMPLATE）",
//       "ask": "改 docs/adr/README.md 與 TEMPLATE.md：「介面動詞」→「介面 recipe」，並把兩檔的相對路徑連結驗證一次，壞的修掉。回報每檔改了哪幾行。",
//       "files": ["docs/adr/README.md", "docs/adr/TEMPLATE.md"]
//     }
//   ],
//   "verify": [
//     {
//       "key": "residue",
//       "label": "驗證：_Avoid_ 詞殘留",
//       "ask": "以根 GLOSSARY.md 的 _Avoid_ 行為準，grep 現行 md 的正文（_Avoid_ 行本身除外），列出每個殘留的位置與詞，並回報掃了幾個檔。"
//     }
//   ],
//   "effort": { "verify": "low" }
// }
