export const meta = {
  name: 'pr',
  description: '把每一項做成一個 PR：開 issue 掛成 sub-issue、開 worktree、修改、verify.py 驗證、commit、開 PR、等 CI，可選 merge 與清理；預設依序，parallel 時同時跑',
  whenToUse: '要開一個或多個「一個 issue 一個 PR」的改動時；依序模式任何一步失敗就停、後面的項目不做，parallel 模式各項獨立、互不影響',
  phases: [
    { title: 'PR', detail: '每一項一個子代理，預設依序、parallel 時同時跑；機械步驟呼叫 script/workflow/ 的腳本（worktree 開好後用 worktree 自己的），會寫入 GitHub 的 gh 指令由子代理逐一下' },
  ],
}

// args: {
//   parent: number,       // 必填，父題的 issue 編號；新 issue 用 `Part of #<parent>` 開並掛成它的 sub-issue
//   items: {              // 必填；預設依序執行，parallel 時同時跑
//     no: number|string,  // 這一項的編號，用於識別與 label
//     branch: string,     // 分支名，worktree 開在 <repoRoot 上一層>/worktree/branch/<branch>
//     title: string,      // issue 標題
//     content: string,    // 要做的內容（給子代理的任務描述）
//     commit: string,     // commit 訊息（第一行是標題，也當 PR 標題）
//     label?: string,     // issue 標籤，預設 'enhancement'
//   }[],
//   merge?: boolean,      // CI 全過後是否 merge 並清理，預設 false
//   parallel?: boolean,   // true＝items 彼此獨立、同時跑，一項失敗不影響其他項；只能配 merge: false。預設 false＝依序、失敗即停
//   repoRoot?: string,    // 主 repo，預設 '/home/cyc/Desktop/vendor-kit_ws/src'
// }
const {
  parent,
  items,
  merge = false,
  parallel: concurrent = false,   // 改名：parallel 是 workflow 內建的並行函式
  repoRoot = '/home/cyc/Desktop/vendor-kit_ws/src',
} = args ?? {}

// ───────────────── 參數檢查 ─────────────────
if (!Number.isInteger(parent) || parent <= 0) {
  throw new Error('args.parent 必填：父題的 issue 編號（正整數），新 issue 會用 `Part of #<parent>` 開並掛成它的 sub-issue')
}
if (!Array.isArray(items) || items.length === 0) {
  throw new Error('args.items 必填：至少一項 { no, branch, title, content, commit, label? }')
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
const dupBranches = [...new Set(items.map(it => it.branch).filter((b, i, a) => a.indexOf(b) !== i))]
if (dupBranches.length) {
  throw new Error(`args.items 的 branch 不能重複：${dupBranches.join('、')}`)
}

const SLUG = 'ycpss91255-research/vendor_kit'
const ws = repoRoot.replace(/\/+$/, '').replace(/\/[^/]+$/, '')
const bodyDir = `${ws}/reference/research/pr`
const S = `${repoRoot}/script/workflow`   // worktree 開好之前用主 repo 的腳本
const nos = items.map(it => it.no).join(',')
log(`pr #${parent} ${nos}${concurrent ? '（並行）' : ''}`)

// ───────────────── 共用規則：組進每個子代理的 prompt ─────────────────
const RULES = `硬性規則（違反就算這一項失敗）：
- 會寫入 GitHub 的動作（gh issue create、sub_issues API、gh pr create、gh pr merge、留言）一律自己逐一下 gh 指令，每個指令都帶 \`-R ${SLUG}\`；不要把它們包進腳本或用 && 串在一起。
- issue 與 PR 的本文一律先寫成檔（放 ${bodyDir}/），先跑 \`python3 ${S}/body.py check …\` 自檢通過，再用 \`--body-file <絕對路徑>\` 送出，送出後刪掉本文檔。本文裡不准有本機絕對路徑，提到檔案用 repo 相對路徑。
- 一個 PR 剛好連一個 issue，只改一類範圍；不要順手改別的東西。
- commit 照 repo 格式（\`type(scope): 摘要\`），footer 帶 \`Refs: #<issue>\`；不加 Claude 署名、Co-Authored-By 或 session 連結。
- 只准 push 到這一項自己的分支；不准 push main、不准 force push main。這一項的分支跟 main 衝突時可以 \`git fetch origin && git rebase origin/main\` 後 \`git push --force-with-lease\`（只限自己的分支）。
- 機械步驟用 script/workflow/ 的腳本，讀它輸出的 JSON 判斷成敗，不要自己重寫一遍。開 worktree 之前用主 repo 的 ${S}/；worktree 開好之後一律用 worktree 自己的 script/（步驟裡寫的路徑），不要用主 repo 的，主 repo 可能落後 main。
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
  const label = it.label ?? 'enhancement'
  const tag = `#${parent}-${it.no}`
  const wt = `${ws}/worktree/branch/${it.branch}`
  const W = `${wt}/script/workflow`   // worktree 開好之後用它自己的腳本
  const issueFile = `${bodyDir}/${parent}-${it.no}-issue.md`
  const prFile = `${bodyDir}/${parent}-${it.no}-pr.md`
  const q = x => x.replace(/["\\$`]/g, m => '\\' + m)   // 放進 shell 雙引號用
  const prTitle = q(it.commit.split('\n')[0])
  const issueTitle = q(it.title)

  const finish = merge
    ? `8. CI 全過（結束碼 0）才 merge：\`gh pr merge <PR> -R ${SLUG} --merge\`。merge 後 \`git -C ${repoRoot} pull --ff-only\`，再 \`python3 ${S}/worktree.py remove ${it.branch} --repo ${repoRoot}\` 清理（只刪 worktree 與本機分支，不刪遠端）。結束碼不是 0 就不 merge、不清理，停下回報。`
    : `8. 不 merge（這次 args.merge 是 false）。worktree 留著，之後要修才用得到；cleaned 回報 false。`

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

${RULES}

步驟（照順序）：
1. 開 issue：本文寫成檔 ${issueFile}（目錄不存在就建），第一行 \`Part of #${parent}\`，接著寫「要做的」與「完成條件」。自檢 \`python3 ${S}/body.py check ${issueFile} --kind issue --parent ${parent}\`，ok 才繼續。用另一個指令 \`gh issue create -R ${SLUG} --title "${issueTitle}" --label ${label} --body-file ${issueFile}\`，記下編號 N。刪掉 ${issueFile}。
2. 掛成 sub-issue：\`gh api repos/${SLUG}/issues/N -q .id\` 取 id，再用另一個指令 \`gh api -X POST repos/${SLUG}/issues/${parent}/sub_issues -F sub_issue_id=<id>\`。
3. 開 worktree：\`python3 ${S}/worktree.py add ${it.branch} --repo ${repoRoot}\`（會先 fetch、從 origin/main 開在 ${wt}；已存在會報錯，報錯就停）。之後都在 ${wt} 裡做。
4. 修改：照「要做的內容」改。
5. 驗證：\`python3 ${W}/verify.py --root ${wt}\`。它跑 docs.yml 每個 \`run:\`、每個 \`script/*/test\` 的 unittest、check_script_layout、hooks 的測試，並檢查每個 \`script/*/test\` 都在 docs.yml 裡；輸出 JSON 的 ok 是 true 才算過。失敗時看 steps 裡 ok 是 false 的 output 自己判斷：是這次改動造成的就修好再重跑一次 verify.py；修不了或跟這次無關就停下，不要 commit，在 error 寫清楚。
6. commit 一個（訊息照上面，最後空一行加 footer \`Refs: #N\`），\`git push -u origin ${it.branch}\`。
7. 開 PR：本文寫成檔 ${prFile}，第一行 \`[claude] \` 開頭寫一句摘要，接著「做了什麼」「為什麼」「驗證」（列實際跑的指令與結果），最後一行 \`Closes #N\`。自檢 \`python3 ${W}/body.py check ${prFile} --kind pr --issue N\`，ok 才送。用另一個指令 \`gh pr create -R ${SLUG} --base main --head ${it.branch} --title "${prTitle}" --body-file ${prFile}\`。刪掉 ${prFile}。
   等 CI：\`python3 ${W}/wait_ci.py <PR>\`（預設最多 600 秒）。結束碼 0＝全過；1＝有失敗：看 \`gh run view --log-failed -R ${SLUG}\`，是這次改動造成的就修、commit、push 後再等一次，修不了就停；2＝逾時，停下回報；跟 main 衝突時照規則 rebase。
${finish}

回報：issue、pr 編號、pr_url、ci_pass（最後一次 wait_ci 是否全過）、merged、cleaned、summary（改了什麼、驗證結果、特別處理）、error（失敗時寫停在哪一步、為什麼）。`, { label: tag, phase: 'PR', schema: RES })

  return { no: it.no, branch: it.branch, ...r }
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
      return { no: it.no, branch: it.branch, ci_pass: false, merged: false, summary: '', error: `子代理失敗：${e?.message ?? e}` }
    }
  }))
  out.push(...rs)
  failed = out.filter(o => !done(o)).map(o => ({ no: o.no, reason: reasonOf(o) }))
  for (const f of failed) log(`#${parent}-${f.no} 沒有完成：${f.reason}`)
} else {
  for (const it of items) {
    const o = await runItem(it)
    out.push(o)
    if (!done(o)) {
      stopped = { no: it.no, reason: reasonOf(o) }
      log(`#${parent}-${it.no} 沒有完成，停下；後面的項目不做`)
      break
    }
  }
}

log(`完成：${out.filter(done).length}/${items.length} 項${stopped ? `，停在 ${stopped.no}` : ''}${failed.length ? `，失敗 ${failed.map(f => f.no).join(',')}` : ''}`)

return { parent, merge, parallel: concurrent, results: out, stopped, failed, skipped: items.slice(out.length).map(it => it.no) }

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
