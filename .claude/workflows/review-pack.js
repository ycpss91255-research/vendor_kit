export const meta = {
  name: 'review-pack',
  description: '送審打包：重產送審副本 → commit → 寫審閱說明 → 打包 zip → commit 送審紀錄；回傳 zip 與每頁本機檔的絕對路徑',
  whenToUse: '要把 PR worktree 裡的審閱頁打包成 review_v<N>.zip 送給維護者時；每次傳 zip 都同時給本機路徑',
  phases: [
    { title: '定位', detail: 'effort low 子代理在 repo 跑 git rev-parse --path-format=absolute --git-common-dir，取其上一層當主 repo，再上一層是 workspace；腳本一律從主 repo 的 script/ 取' },
    { title: '重產', detail: '在 repo 跑 script/doc/mark_changes.py <pages>，再用 script/doc/review_paths.py pages 取送審資料夾、版號、基準與這次的 zip 號（打包前取）' },
    { title: 'commit 副本', detail: 'script/git/commit_push.py --add 有改動的送審資料夾，標題「docs(review): 重產送審副本」；副本沒有改動就跳過' },
    { title: '審閱說明', detail: 'Claude 子代理依 noteBrief 寫 <workspace>/reference/research/batch3/00_審閱說明_v<N>.md，結尾附 JS 組好的版本表' },
    { title: '打包', detail: 'script/doc/pack_review.py --note <說明> --out <workspace>/reference/review_sent/ <pages>，再用 review_paths.py zip 列出 zip 內容；zip 號要等於打包前算的 N' },
    { title: 'commit 送審紀錄', detail: 'script/git/commit_push.py --add doc/review/versions.json，標題「chore(review): 送審 review_v<N>」' },
  ],
}

// args 契約：
//   repo       string    必填，PR worktree 的絕對路徑（例如 .../worktree/pr/59）；重產、打包、commit 都在這裡做
//   branch     string    必填，repo 目前的分支；commit_push.py 會確認一致，push 到這個分支
//   pages      string[]  必填，頁鍵（寫法同 versions.json 與 mark_changes.py），例如 ["02_invariants","GLOSSARY.md"]
//   refs       number[]  必填，commit footer 的 issue 編號；第一個交給 commit_push.py --refs，其餘寫進訊息的 footer 段
//   noteBrief  string    必填，審閱說明要寫的內容（這次改了什麼、待確認、更正等），子代理照寫
//   notePrev   string    可省，上一版審閱說明的絕對路徑，供沿用格式
// 機械步驟都由子代理呼叫主 repo 的腳本、照抄輸出；成敗與回傳值由 JS 讀腳本印出的 JSON 判斷與組合。
const { repo: repoArg, branch, pages, refs, noteBrief, notePrev = '' } = args ?? {}

// ───────────────── 參數檢查 ─────────────────
const trimDir = x => String(x ?? '').trim().replace(/\/+$/, '')
const repo = trimDir(repoArg)
if (!repo.startsWith('/')) throw new Error(`args.repo 必填，PR worktree 的絕對路徑（收到 ${JSON.stringify(repoArg)}）`)
if (typeof branch !== 'string' || !branch.trim() || branch.trim() === 'main') throw new Error('args.branch 必填，repo 目前的分支（不能是 main）')
if (!Array.isArray(pages) || pages.length === 0 || pages.some(p => typeof p !== 'string' || !/^[A-Za-z0-9_./-]+$/.test(p))) {
  throw new Error('args.pages 必填：頁鍵陣列，例如 ["02_invariants","03_output","GLOSSARY.md"]（只能有英數、底線、點、斜線、連字號）')
}
if (new Set(pages).size !== pages.length) throw new Error('args.pages 有重複的頁鍵')
if (!Array.isArray(refs) || refs.length === 0 || refs.some(n => !Number.isInteger(n) || n < 1)) {
  throw new Error('args.refs 必填：issue 編號陣列（正整數），例如 [141, 350]')
}
if (typeof noteBrief !== 'string' || !noteBrief.trim()) throw new Error('args.noteBrief 必填：審閱說明要寫的內容')
if (typeof notePrev !== 'string' || (notePrev.trim() && !notePrev.trim().startsWith('/'))) {
  throw new Error(`args.notePrev 只能是絕對路徑（收到 ${JSON.stringify(notePrev)}）`)
}
const BR = branch.trim()
const PAGES = pages.join(' ')
log(`review-pack ${BR} ${pages.join('、')}`)
// 暫存檔放子代理 scratchpad 的這個子目錄：同時跑幾次 review-pack 時檔名不會互蓋
const TMP = `<你的 scratchpad>/review-pack/${BR.replace(/[^A-Za-z0-9_-]+/g, '_')}`

// ───────────────── 共用的子代理：照順序跑指令、照抄輸出 ─────────────────
const RUNS = {
  type: 'object',
  properties: {
    runs: { type: 'array', items: { type: 'object', properties: { exit: { type: 'integer' }, output: { type: 'string' } }, required: ['exit', 'output'] } },
    error: { type: 'string' },
  },
  required: ['runs'],
}
// pre：跑指令前要先做的事（例如用 Write 寫訊息檔）
const runCmds = (label, phaseName, cmds, pre = '') => agent(`你的工作是照順序執行下面的指令並照抄輸出，**你自己不判斷成敗、不修任何東西、不重跑**。不改任何檔（除了下面明說要寫的暫存檔），不自己下 git commit、git push 或任何 gh 指令。
${pre}
依序用前景 Bash（timeout 600000）執行，每一行一字不差：
${cmds.map((c, i) => `${i + 1}. \`${c}\``).join('\n')}

每一行執行完把結束碼與完整輸出（stdout 與 stderr，原樣、不刪減）依序填進 runs 的一筆 { exit, output }。某一行結束碼不是 0 就停，後面的不跑。跑不起來就把原因寫進 error。`,
  { label: `review-pack ${label}`, phase: phaseName, schema: RUNS, effort: 'low' })

// 取輸出裡最後一行能解析的 JSON
const lastJson = text => {
  const lines = String(text ?? '').split('\n').map(s => s.trim()).filter(Boolean).reverse()
  for (const l of lines) {
    if (!l.startsWith('{')) continue
    try { return JSON.parse(l) } catch { /* 下一行 */ }
  }
  return null
}

const result = {
  ok: false, repo, main: null, workspace: null, branch: BR, zip: null, zip_files: [], local_files: [],
  note: null, versions: [], commits: { copies: null, versions: null }, stopped: null, error: null,
}
const stop = (step, error) => {
  result.stopped = step
  result.error = error
  log(`停在 ${step}：${error}`)
  return result
}

// commit 訊息：其餘 refs 寫成最後一段 footer，commit_push.py 會把 Refs: #<refs[0]> 接在同一段
const message = (title, body) => [title, '', ...(body.length ? [...body, ''] : []), ...refs.slice(1).map(n => `Refs: #${n}`)].join('\n').trim()
const commitStep = async (label, phaseName, file, msg, add) => {
  const path = `${TMP}/${file}`
  const r = await runCmds(label, phaseName,
    [`python3 ${result.main}/script/git/commit_push.py --repo ${repo} --branch ${BR} --message-file ${path} --refs ${refs[0]} --add ${add.join(' ')}`],
    `先 mkdir -p ${TMP}（\`<你的 scratchpad>\` 換成你 scratchpad 的絕對路徑，下面指令裡的也一樣），再用 Write 工具把下面這段 commit 訊息原樣寫成 ${path}（不要用 heredoc、不要加署名或 Co-Authored-By）：
---
${msg}
---`)
  const j = lastJson(r?.runs?.[0]?.output)
  if (!j) return { ok: false, error: `commit_push.py 沒有輸出 JSON：${r?.error || String(r?.runs?.[0]?.output ?? '').slice(-800)}` }
  if (!j.ok) return { ok: false, error: `commit_push.py 失敗（step ${j.step}）：${[j.error, j.problems?.length && JSON.stringify(j.problems), j.denied?.length && `hook 擋下 ${JSON.stringify(j.denied)}`].filter(Boolean).join('；')}` }
  if (!j.pushed) return { ok: false, error: 'commit_push.py 回報沒有 push' }
  return { ok: true, sha: j.commit }
}

// ───────────────── 定位 ─────────────────
phase('定位')
const loc = await agent(`只做一件事：執行 \`git -C ${repo} rev-parse --path-format=absolute --git-common-dir\`，把印出的那一行原樣填進 common_dir。不改任何檔案、不 commit、不 push。指令失敗就把 common_dir 留空、錯誤訊息寫進 error。`,
  { label: 'review-pack 定位', phase: '定位', effort: 'low',
    schema: { type: 'object', properties: { common_dir: { type: 'string' }, error: { type: 'string' } }, required: ['common_dir'] } })
const common = trimDir(loc?.common_dir)
if (!common.startsWith('/') || !/\/[^/]+$/.test(common)) return stop('定位', `找不到主 repo：${loc?.error || common || '沒有輸出'}`)
result.main = common.replace(/\/[^/]+$/, '')
result.workspace = result.main.replace(/\/[^/]+$/, '')
const DOC = `${result.main}/script/doc`
log(`repo ${repo}；main ${result.main}（腳本 ${DOC}）；workspace ${result.workspace}`)

// ───────────────── 重產 ─────────────────
phase('重產')
const regen = await runCmds('重產', '重產', [
  `cd ${repo} && python3 ${DOC}/mark_changes.py ${PAGES}`,
  `python3 ${DOC}/review_paths.py pages --repo ${repo} ${PAGES}`,
])
if (!regen?.runs?.length || regen.runs[0].exit !== 0) {
  return stop('重產', `mark_changes.py 失敗：${regen?.error || String(regen?.runs?.[0]?.output ?? '沒有輸出').slice(-1500)}`)
}
const paths = lastJson(regen.runs[1]?.output)
if (!paths?.ok || !Array.isArray(paths.pages)) {
  return stop('重產', `review_paths.py pages 失敗：${paths?.error || String(regen.runs[1]?.output ?? '沒有輸出').slice(-800)}`)
}
const N = paths.zip_next
const baseText = b => (b?.kind === 'finalized' ? `v${b.v}（定案版）` : b?.kind === 'replied' ? `v${b.v}（你上次回覆的版本）` : '無（整份標新增）')
result.versions = paths.pages.map(p => ({ name: p.name, key: p.key, version: p.version, base: p.base }))
log(`這包是 review_v${N}：${result.versions.map(v => `${v.key} v${v.version}（基準 ${baseText(v.base)}）`).join('、')}`)

// ───────────────── commit 副本 ─────────────────
phase('commit 副本')
const dirtyDirs = paths.pages.map(p => p.rel_dir).filter(d => paths.dirty.some(line => line.includes(`${d}/`)))
if (!dirtyDirs.length) {
  log('送審副本跟 HEAD 一樣，跳過「重產送審副本」的 commit')
} else {
  const body = paths.pages.filter(p => dirtyDirs.includes(p.rel_dir)).map(p => `- ${p.key}：基準 ${baseText(p.base)}`)
  const c = await commitStep('commit 副本', 'commit 副本', 'copies-msg.txt', message('docs(review): 重產送審副本', body), dirtyDirs)
  if (!c.ok) return stop('commit 副本', c.error)
  result.commits.copies = c.sha
}

// ───────────────── 審閱說明 ─────────────────
phase('審閱說明')
const NOTE = `${result.workspace}/reference/research/batch3/00_審閱說明_v${N}.md`
const table = [
  '| 頁 | 這包的版本 | 基準 |',
  '|---|---|---|',
  ...paths.pages.map(p => `| ${p.key} | v${p.version} | ${baseText(p.base)} |`),
].join('\n')
const note = await agent(`你負責寫一份送給維護者的審閱說明。不改 repo、不 commit、不 push，只寫下面這一個檔。

檔案：${NOTE}（用 Write 工具寫；目錄不存在先 mkdir -p）
${notePrev.trim() ? `格式沿用上一版：先讀 ${notePrev.trim()}，標題、節次與語氣照它。\n` : ''}第一行是 \`# review_v${N} 審閱說明\`。接著依下面的內容寫，不要自己加沒給的事實：
---
${noteBrief.trim()}
---
最後一節是「## 各檔版本」，先寫一句「紅綠只標跟基準版之間的改動。」，再把下面這張表原樣貼上（版本由腳本算，不要改數字）：
${table}

用繁體中文、直接寫結論，對維護者用「你」。寫完回報 path（實際寫入的絕對路徑）。`,
  { label: 'review-pack 審閱說明', phase: '審閱說明',
    schema: { type: 'object', properties: { path: { type: 'string' }, error: { type: 'string' } }, required: ['path'] } })
if (trimDir(note?.path) !== NOTE) return stop('審閱說明', `審閱說明沒有寫到 ${NOTE}：${note?.error || note?.path || '沒有回報'}`)
result.note = NOTE

// ───────────────── 打包 ─────────────────
phase('打包')
const OUT = `${result.workspace}/reference/review_sent`
const ZIP = `${OUT}/review_v${N}.zip`
const packed = await runCmds('打包', '打包', [
  `cd ${repo} && python3 ${DOC}/pack_review.py --note ${NOTE} --out ${OUT}/ ${PAGES}`,
  `python3 ${DOC}/review_paths.py zip ${ZIP}`,
])
if (!packed?.runs?.length || packed.runs[0].exit !== 0) {
  return stop('打包', `pack_review.py 失敗：${packed?.error || String(packed?.runs?.[0]?.output ?? '沒有輸出').slice(-1500)}`)
}
const firstLine = String(packed.runs[0].output ?? '').split('\n').map(s => s.trim()).find(Boolean) ?? ''
if (firstLine.replace(/\/+/g, '/') !== ZIP) return stop('打包', `pack_review.py 產出 ${firstLine}，跟打包前算的 ${ZIP} 不同；versions.json 可能已改，先檢查再 commit`)
const zj = lastJson(packed.runs[1]?.output)
if (!zj?.ok) return stop('打包', `review_paths.py zip 失敗：${zj?.error || String(packed.runs[1]?.output ?? '沒有輸出').slice(-800)}`)
result.zip = zj.zip
result.zip_files = zj.files
result.local_files = paths.pages.map(p => ({ key: p.key, dir: p.dir, files: p.files }))

// ───────────────── commit 送審紀錄 ─────────────────
phase('commit 送審紀錄')
const v = await commitStep('commit 送審紀錄', 'commit 送審紀錄', 'versions-msg.txt', message(`chore(review): 送審 review_v${N}`, []), ['doc/review/versions.json'])
if (!v.ok) return stop('commit 送審紀錄', v.error)
result.commits.versions = v.sha
result.ok = true
log(`完成：${result.zip}（${result.zip_files.length} 個檔）；審閱說明 ${NOTE}`)
return result

// ───────────────── args 範例（可直接貼進 Workflow 的 args） ─────────────────
// {
//   "repo": "<workspace>/worktree/pr/59",
//   "branch": "docs/contract-review",
//   "pages": ["02_invariants", "03_output", "04_interface", "GLOSSARY.md"],
//   "refs": [141, 350],
//   "noteBrief": "這包有四頁：02、03、04、GLOSSARY。02、03 定案後又有修正：……。04 移除所有 VKxxxx 代碼引用……。待確認：……",
//   "notePrev": "<workspace>/reference/research/batch3/00_審閱說明_v11.md"
// }
