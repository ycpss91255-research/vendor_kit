export const meta = {
  name: 'pr',
  description: '把每一項做成一個 PR（每項可各自指定父題）：開 issue 掛成 sub-issue、開 worktree、修改、verify.py 驗證、commit、開 PR、等 CI，可選 merge 與清理；預設依序，parallel 時同時跑',
  whenToUse: '要開一個或多個「一個 issue 一個 PR」的改動時；依序模式任何一步失敗就停、後面的項目不做，parallel 模式各項獨立、互不影響',
  phases: [
    { title: '準備', detail: '沒給 repoRoot 時，派 effort low 的子代理用 git rev-parse --git-common-dir 查出主 repo' },
    { title: 'PR', detail: '每一項一個子代理，預設依序、parallel 時同時跑；issue_open.py 開 issue 並掛 sub-issue；verify.py 驗證；commit_push.py commit 並 push；pr_open.py 開 PR；wait_ci.py --failed-logs 等 CI；merge 時 merge_pr.py。寫入都由腳本在寫入前經 hook 檢查' },
  ],
}

// args: {
//   parent?: number,      // 預設的父題 issue 編號；新 issue 用 `Part of #<parent>` 開並掛成它的 sub-issue。每個 item 都帶 parent 時可省
//   items: {              // 必填；預設依序執行，parallel 時同時跑（不同父題的項目也可以）
//     no: number|string,  // 這一項的編號，用於識別、label 與暫存目錄；同一父題內不能重複
//     parent?: number,    // 這一項的父題，不給就用最上層的 parent
//     branch: string,     // 分支名，worktree 開在 <repoRoot 上一層>/worktree/branch/<branch>
//     title: string,      // issue 標題
//     content: string,    // 要做的內容（給子代理的任務描述）
//     commit: string,     // commit 訊息（第一行是標題，也當 PR 標題）
//     label?: string,     // issue 標籤，預設 'enhancement'
//   }[],
//   merge?: boolean,      // CI 全過後是否 merge 並清理，預設 false
//   parallel?: boolean,   // true＝items 彼此獨立、同時跑，一項失敗不影響其他項；只能配 merge: false。預設 false＝依序、失敗即停
//   repoRoot?: string,    // 主 repo；不給就由子代理跑 `git rev-parse --path-format=absolute --git-common-dir` 取上一層（linked worktree 也回到主 repo）
// }
const {
  parent,
  items,
  merge = false,
  parallel: concurrent = false,   // 改名：parallel 是 workflow 內建的並行函式
  repoRoot: repoArg,
} = args ?? {}

// ───────────────── 參數檢查 ─────────────────
const isIssueNo = n => Number.isInteger(n) && n > 0
if (parent !== undefined && !isIssueNo(parent)) {
  throw new Error('args.parent 要是正整數：預設的父題 issue 編號，新 issue 會用 `Part of #<parent>` 開並掛成它的 sub-issue')
}
if (!Array.isArray(items) || items.length === 0) {
  throw new Error('args.items 必填：至少一項 { no, branch, title, content, commit, parent?, label? }')
}
const badParents = items
  .map((it, i) => ({ i, p: it?.parent }))
  .filter(x => x.p !== undefined && !isIssueNo(x.p))
if (badParents.length) {
  throw new Error(`args.items 的 parent 要是正整數：${badParents.map(x => `第 ${x.i + 1} 項是 ${JSON.stringify(x.p)}`).join('；')}`)
}
const parentOf = it => it?.parent ?? parent
const orphans = items.map((it, i) => i).filter(i => !isIssueNo(parentOf(items[i])))
if (orphans.length) {
  throw new Error(`第 ${orphans.map(i => i + 1).join('、')} 項沒有父題：在該項帶 parent，或給最上層的 args.parent（不給的項目用它）`)
}
const badItems = items
  .map((it, i) => ({
    i,
    miss: [
      ...((typeof it?.no === 'number' || (typeof it?.no === 'string' && it.no.trim())) ? [] : ['no']),
      ...['branch', 'title', 'content', 'commit'].filter(k => typeof it?.[k] !== 'string' || !it[k].trim()),
    ],
  }))
  .filter(x => x.miss.length)
if (badItems.length) {
  throw new Error(`args.items 有項目缺欄位：${badItems.map(x => `第 ${x.i + 1} 項缺 ${x.miss.join('、')}`).join('；')}`)
}
if (typeof merge !== 'boolean') {
  throw new Error('args.merge 要是布林值：true＝CI 全過後 merge 並清理；false（預設）＝停在等 merge')
}
if (typeof concurrent !== 'boolean') {
  throw new Error('args.parallel 要是布林值：true＝items 同時跑、互不影響；false（預設）＝依序、失敗即停')
}
if (concurrent && merge) {
  throw new Error('args.parallel 為 true 時 args.merge 必須是 false：多個 PR 同時 merge 會互相衝突，交給主對話依序 merge')
}
if (repoArg !== undefined && (typeof repoArg !== 'string' || !repoArg.trim())) {
  throw new Error('args.repoRoot 要是非空字串（主 repo 的絕對路徑）；不給就由子代理查出')
}
const dupBranches = [...new Set(items.map(it => it.branch).filter((b, i, a) => a.indexOf(b) !== i))]
if (dupBranches.length) {
  throw new Error(`args.items 的 branch 不能重複：${dupBranches.join('、')}`)
}
// 暫存目錄以 <父題>-<no> 命名，同一父題的 no 重複就會共用目錄、互相覆蓋
const tagOf = it => `${parentOf(it)}-${String(it.no).trim()}`
const dupTags = [...new Set(items.map(tagOf).filter((t, i, a) => a.indexOf(t) !== i))]
if (dupTags.length) {
  throw new Error(`同一父題內 items 的 no 不能重複：${dupTags.map(t => `#${t}`).join('、')}`)
}

const SLUG = 'ycpss91255-research/vendor_kit'

// ───────────────── 準備：沒給 repoRoot 就由子代理查出主 repo ─────────────────
let repoRoot = repoArg?.trim()
if (!repoRoot) {
  phase('準備')
  const found = await agent(`在你的工作目錄跑 \`git rev-parse --path-format=absolute --git-common-dir\`，只跑這一個指令，不要改任何東西。
它印出主 repo 的 .git 目錄（在 linked worktree 裡跑也一樣是主 repo 的）。回報：ok（指令成功且輸出是以 /.git 結尾的絕對路徑）、git_dir（輸出原樣）、error（失敗時照抄錯誤訊息）。`,
    { label: '查 repoRoot', phase: '準備', schema: {
      type: 'object',
      properties: { ok: { type: 'boolean' }, git_dir: { type: 'string' }, error: { type: 'string' } },
      required: ['ok'],
    }, agentType: 'general-purpose', effort: 'low' })
  const gd = (found?.git_dir ?? '').trim().replace(/\/+$/, '')
  if (!found?.ok || !gd.startsWith('/') || !gd.endsWith('/.git')) {
    throw new Error(`查不到 repoRoot：${found?.error || `git-common-dir 輸出不是 <repo>/.git：${gd || '（空）'}`}；請明確帶 args.repoRoot`)
  }
  repoRoot = gd.replace(/\/\.git$/, '')
}
repoRoot = repoRoot.replace(/\/+$/, '')

const ws = repoRoot.replace(/\/+$/, '').replace(/\/[^/]+$/, '')
const S = `${repoRoot}/script/workflow`   // worktree 開好之前用主 repo 的腳本
const RH = `${repoRoot}/script/github`
const parents = [...new Set(items.map(parentOf))]
const heading = parents
  .map(p => `#${p} ${items.filter(it => parentOf(it) === p).map(it => it.no).join(',')}`)
  .join('；')
log(`pr ${heading}${concurrent ? '（並行）' : ''}`)

// ───────────────── 共用規則：組進每個子代理的 prompt ─────────────────
const RULES = `硬性規則（違反就算這一項失敗）：
- GitHub 寫入與 commit／push 一律用下面步驟寫的腳本，它們在寫入前用 .claude/settings.json 註冊的同一批 Bash hook 檢查；不要自己下 gh issue create、gh api sub_issues、gh pr create、gh pr merge、git commit、git push。腳本 ok 是 false 就照它 JSON 的 step、problems、denied、error 停下回報，不要自己改用別的指令補做寫入。
- issue 與 PR 的本文、issue 標題、commit 訊息一律先用 Write 工具寫成檔（放這一項的暫存目錄，見下一條），再把檔交給腳本；腳本自己做自檢，送出成功後會刪掉本文檔。本文裡不准有本機絕對路徑，提到檔案用 repo 相對路徑。
- 暫存檔（commit 訊息、issue 標題、issue／PR 本文、一次性腳本、輸出紀錄）一律放這一項自己的暫存目錄（步驟裡寫的 \`<你的 scratchpad>/pr/<父題>-<編號>/\`，先 mkdir -p），\`<你的 scratchpad>\` 換成你 scratchpad 的絕對路徑；不要放 scratchpad 根目錄，也不要用別的子代理也可能用的檔名：同時可能有其他項目的子代理在跑，並行的子代理共用同一個 scratchpad，固定檔名會互相覆蓋（#234、#235 互蓋過）。
- 一個 PR 剛好連一個 issue，只改一類範圍；不要順手改別的東西。
- commit 照 repo 格式（\`type(scope): 摘要\`）；footer \`Refs: #<issue>\` 由 commit_push.py 加；不加 Claude 署名、Co-Authored-By 或 session 連結。
- 只准 push 到這一項自己的分支；不准 push main、不准 force push main。只有需要 rebase（PR 跟 main 衝突，或 push 被拒且原因是跟 origin/main 衝突）時才跑步驟裡寫的 rebase_push.py（fetch、rebase origin/main、\`--force-with-lease\` 推回這一項的分支）；JSON 的 state 是 conflict 時照 conflicts 解衝突（這是要判斷的），\`git add\` 解好的檔後跑同一行加 \`--continue\`，直到 state 是 rebased 或 up_to_date；ok 是 false 就停下回報。
- 機械步驟用 script/ 的腳本，讀它輸出的 JSON 判斷成敗，不要自己重寫一遍。開 worktree 之前用主 repo 的 ${repoRoot}/script/；worktree 開好之後一律用 worktree 自己的 script/（步驟裡寫的路徑），不要用主 repo 的，主 repo 可能落後 main；merge 與收尾的 merge_pr.py 例外，用主 repo 的，因為它會移除 worktree。
- 子代理自己判斷的只有兩件事：怎麼修改，以及驗證失敗時要修還是停下。其他步驟照順序做，任何一步失敗就停下回報，不要 merge。`

const RES = {
  type: 'object',
  properties: {
    issue: { type: 'integer' },
    pr: { type: 'integer' },
    pr_url: { type: 'string' },
    ci_pass: { type: 'boolean' },
    merged: { type: 'boolean' },
    cleaned: { type: 'boolean' },
    summary: { type: 'string' },
    error: { type: 'string' },
  },
  required: ['ci_pass', 'merged', 'summary'],
}

// 跑一項：回傳子代理的結果，加上 no 與 branch
async function runItem(it) {
  const parent = parentOf(it)
  const label = it.label ?? 'enhancement'
  const tag = `#${tagOf(it)}`
  const wt = `${ws}/worktree/branch/${it.branch}`
  const W = `${wt}/script/workflow`   // worktree 開好之後用它自己的腳本
  const G = `${wt}/script/git`
  const H = `${wt}/script/github`
  // 並行的子代理共用同一個 scratchpad：暫存檔一律放以 <父題>-<no> 命名的子目錄（#241）
  const item = tagOf(it).replace(/[\/\s:]+/g, '_')
  const tmp = `<你的 scratchpad>/pr/${item}`
  const issueFile = `${tmp}/issue.md`
  const titleFile = `${tmp}/title.txt`
  const prFile = `${tmp}/pr.md`
  const msgFile = `${tmp}/commit-msg.txt`
  const rebase = `python3 ${G}/rebase_push.py --repo ${wt} --branch ${it.branch}`

  const finish = merge
    ? `7. CI 全過（結束碼 0）才 merge 並收尾：\`python3 ${repoRoot}/script/workflow/merge_pr.py <PR> --repo ${repoRoot} --scratch <你的 scratchpad> --item ${item}\`（\`<你的 scratchpad>\` 換成 scratchpad 根目錄的絕對路徑）。它再確認一次 CI 與 head 沒變、merge（只用 --merge）、pull 主 repo、移除 worktree 與本機分支、刪 ${tmp}/。JSON 的 ok 是 true 才回報 merged、cleaned 為 true；ok 是 false 時 merged 照 JSON 的 merged、cleaned 回報 false，照 error 停下回報。等 CI 的結束碼不是 0 就不跑它，停下回報。`
    : `7. 不 merge（這次 args.merge 是 false）。worktree 留著，之後要修才用得到；cleaned 回報 false。`

  const r = await agent(`${tag}：把下面這一項做成一個 PR。父題 ${SLUG}#${parent}（\`gh issue view ${parent} -R ${SLUG}\` 讀背景）。主 repo ${repoRoot}。

這一項：
- 分支：\`${it.branch}\`
- issue 標題：${it.title}
- issue 標籤：${label}
- commit 訊息：
\`\`\`
${it.commit}
\`\`\`
- 要做的內容：${it.content}
- 暫存目錄：${tmp}/

${RULES}

步驟（照順序）：
1. 開 issue 並掛成 sub-issue：先 \`mkdir -p ${tmp}\`。用 Write 把 issue 標題（上面「issue 標題」那一行原樣，不加引號）寫成 ${titleFile}；本文寫成 ${issueFile}，第一行 \`Part of #${parent}\`，接著寫「要做的」與「完成條件」。跑 \`python3 ${RH}/issue_open.py create --title-file ${titleFile} --label ${label} --body-file ${issueFile} --parent ${parent}\`：它自檢本文、開 issue、掛到 #${parent}，每個寫入前經 hook 檢查，開成功就刪掉本文檔。JSON 的 issue 就是 N。結束碼 0 才繼續；3＝issue 已開但掛 sub-issue 失敗，跑一次 \`python3 ${RH}/issue_open.py attach --parent ${parent} --issue N\`，還是失敗就停（不要再 create）；其他結束碼照 step、problems、denied、error 停下回報。
2. 開 worktree：\`python3 ${S}/worktree.py add ${it.branch} --repo ${repoRoot}\`（會先 fetch、從 origin/main 開在 ${wt}；已存在會報錯，報錯就停）。之後都在 ${wt} 裡做。
3. 修改：照「要做的內容」改。
4. 驗證：\`python3 ${W}/verify.py --root ${wt}\`。它跑 docs.yml 每個 \`run:\`、每個 \`script/*/test\` 的 unittest、check_script_layout、hooks 的測試，並檢查每個 \`script/*/test\` 都在 docs.yml 裡；輸出 JSON 的 ok 是 true 才算過。失敗時看 steps 裡 ok 是 false 的 output 自己判斷：是這次改動造成的就修好再重跑一次 verify.py；修不了或跟這次無關就停下，不要 commit，在 error 寫清楚。
5. commit 一個並 push：用 Write 把上面的 commit 訊息原樣（不含 footer）寫成 ${msgFile}，跑 \`python3 ${G}/commit_push.py --repo ${wt} --branch ${it.branch} --message-file ${msgFile} --refs N --all\`。它檢查訊息、補 footer \`Refs: #N\`、\`git add -A\`、commit、push 到 ${it.branch}，每個寫入前經 hook 檢查。JSON 的 ok 是 true 才算 commit 與 push 成功；push 被拒且原因是跟 origin/main 衝突時跑 \`${rebase}\`（規則見上）。
6. 開 PR 並等 CI：本文寫成 ${prFile}，第一行 \`[claude] \` 開頭寫一句摘要，接著「做了什麼」「為什麼」「驗證」（列實際跑的指令與結果），最後一行 \`Closes #N\`。跑 \`python3 ${H}/pr_open.py --repo ${wt} --branch ${it.branch} --issue N --body-file ${prFile} --title-from-commit\`：它確認分支已推齊、沒有重複的 PR，用 HEAD 的 commit 標題當 PR 標題，自檢標題、本文與 PR 規則（改動檔由腳本自己取），經 hook 檢查後開 PR，成功就刪掉本文檔。JSON 的 ok 是 true 才繼續，pr 與 url 就是 PR 編號與網址；ok 是 false 就照 step、problems、denied、error 停下回報。
   等 CI：\`python3 ${W}/wait_ci.py <PR> --failed-logs\`（預設最多 600 秒）。結束碼 0＝全過；1＝有失敗：看 JSON 的 failed_logs（每個失敗 check 的日誌尾段 tail；tail 是 null 時看 error），是這次改動造成的就修，修好後重跑一次 verify.py，再照第 5 步用同一個訊息檔跑同一行 commit_push.py，再等一次，修不了就停；2＝逾時，停下回報。跟 main 衝突時跑 \`${rebase}\`（規則見上）後再等一次。
${finish}

回報：issue、pr 編號、pr_url、ci_pass（最後一次 wait_ci 是否全過）、merged、cleaned、summary（改了什麼、驗證結果、特別處理）、error（失敗時寫停在哪一步、為什麼）。`, { label: tag, phase: 'PR', schema: RES })

  return { no: it.no, parent, branch: it.branch, ...r }
}

const done = o => !!(o && o.ci_pass && (!merge || o.merged))
const reasonOf = o => o?.error || (merge ? '沒有 merge' : 'CI 沒有全過')

const out = []
let stopped = null
let failed = []
if (concurrent) {
  // 各項獨立：一項的子代理失敗或丟錯，只記在它自己的結果，不影響其他項
  const rs = await parallel(items.map(it => async () => {
    try {
      return await runItem(it)
    } catch (e) {
      return { no: it.no, parent: parentOf(it), branch: it.branch, ci_pass: false, merged: false, summary: '', error: `子代理失敗：${e?.message ?? e}` }
    }
  }))
  out.push(...rs)
  failed = out.filter(o => !done(o)).map(o => ({ no: o.no, parent: o.parent, reason: reasonOf(o) }))
  for (const f of failed) log(`#${f.parent}-${f.no} 沒有完成：${f.reason}`)
} else {
  for (const it of items) {
    const o = await runItem(it)
    out.push(o)
    if (!done(o)) {
      stopped = { no: it.no, parent: o.parent, reason: reasonOf(o) }
      log(`#${o.parent}-${it.no} 沒有完成，停下；後面的項目不做`)
      break
    }
  }
}

log(`完成：${out.filter(done).length}/${items.length} 項${stopped ? `，停在 ${stopped.no}` : ''}${failed.length ? `，失敗 ${failed.map(f => f.no).join(',')}` : ''}`)

return { parent: parent ?? null, parents, merge, parallel: concurrent, results: out, stopped, failed, skipped: items.slice(out.length).map(it => it.no) }

// ───────────────── args 範例（可直接貼進 Workflow 的 args） ─────────────────
// {
//   "parent": 140,
//   "merge": false,
//   "parallel": false,
//   "items": [
//     {
//       "no": 1,
//       "branch": "feat/check-links",
//       "title": "script/doc/check_links.py：檢查 md 的相對連結",
//       "content": "新增 script/doc/check_links.py：掃 git ls-files 的 .md，相對連結的目標檔與錨點要解得開；附 script/doc/test/ 的 unittest；docs.yml 的 docs-lint 加一步跑它；script/doc/README.md 補一節。",
//       "commit": "feat(doc): check_links 檢查 md 的相對連結",
//       "label": "enhancement"
//     }
//   ]
// }
//
// 各自父題、同時跑（最上層 parent 可省）：
// {
//   "parallel": true,
//   "items": [
//     { "no": 1, "parent": 140, "branch": "feat/a", "title": "…", "content": "…", "commit": "feat(doc): …" },
//     { "no": 1, "parent": 241, "branch": "feat/b", "title": "…", "content": "…", "commit": "feat(workflow): …" }
//   ]
// }
