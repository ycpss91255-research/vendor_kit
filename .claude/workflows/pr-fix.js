export const meta = {
  name: 'pr-fix',
  description: '在已開 PR 的 worktree 修一個問題：準備 worktree → 修改 → 驗證 → 一個 commit → push → 等 CI；不 merge',
  whenToUse: 'PR 已經開了、CI 或審查要求再改時；一次修一個問題，CI 通過就停',
  phases: [
    { title: '準備', detail: 'pr_target.py 查分支、worktree、issue，並確認 worktree 乾淨且在 PR 分支最新' },
    { title: '修改', detail: '子代理在 worktree 修改；verify.py 跑全部驗證；commit、push；wait_ci.py 等 CI' },
  ],
}

// args: {
//   pr: number,        // 必填，PR 編號；分支、worktree、issue 由 script/workflow/pr_target.py 查
//   problem: string,   // 必填，要修的問題
//   todo: string,      // 必填，要做的事（給子代理的任務描述）
//   commit: string,    // 必填，commit 訊息第一行（type(scope): 摘要），footer 由 workflow 補 Refs: #<issue>
//   repoRoot?: string, // 主 repo；不給就用子代理的工作目錄（主 repo 根目錄），由 pr_target.py 回報實際位置
// }
const {
  pr,
  problem,
  todo,
  commit,
  repoRoot,
} = args ?? {}

// ───────────────── 參數檢查 ─────────────────
if (!Number.isInteger(pr) || pr <= 0) {
  throw new Error('args.pr 必填：PR 編號（正整數）')
}
const missing = [['problem', problem], ['todo', todo], ['commit', commit]]
  .filter(([, v]) => typeof v !== 'string' || !v.trim())
  .map(([k]) => k)
if (missing.length) {
  throw new Error(`args 缺必填欄位：${missing.join('、')}（problem＝要修的問題、todo＝要做的事、commit＝commit 訊息第一行）`)
}
if (commit.includes('\n')) {
  throw new Error('args.commit 只放 commit 訊息第一行（type(scope): 摘要）；footer Refs: #<issue> 由 workflow 補')
}

const SLUG = 'ycpss91255-research/vendor_kit'
const tag = `#${pr}`
const q = x => x.replace(/["\\$`]/g, m => '\\' + m)   // 放進 shell 雙引號用
log(`pr-fix #${pr}`)

// ───────────────── 準備：查分支、worktree、issue ─────────────────
const TARGET = {
  type: 'object',
  properties: {
    ok: { type: 'boolean' },
    branch: { type: 'string' },
    issue: { type: 'integer' },
    repo: { type: 'string' },
    path: { type: 'string' },
    url: { type: 'string' },
    created: { type: 'boolean' },
    behind_main: { type: 'integer' },
    error: { type: 'string' },
  },
  required: ['ok'],
}

phase('準備')
const prep = repoRoot
  ? `python3 ${repoRoot}/script/workflow/pr_target.py ${pr} --repo ${repoRoot}`
  : `python3 script/workflow/pr_target.py ${pr}`
const t = await agent(`${tag} 準備：只跑一個指令，不要改任何檔。${repoRoot ? '' : '在你的工作目錄（主 repo 根目錄）執行。'}

\`${prep}\`

它會用唯讀的 \`gh pr view\` 查 PR 分支與本文、從本文取第一個 Closes／Refs #N 當 issue、在 worktree/branch/<分支> 找或建 worktree，並確認 worktree 乾淨、在 PR 分支最新（落後就 fast-forward）。
把它輸出的那一行 JSON 原樣照欄位回報（ok、branch、issue、repo、path、url、created、behind_main、error）。ok 是 false 就照抄 error，不要自己補救、不要重試別的寫法。`, { label: `${tag} 準備`, phase: '準備', schema: TARGET })

if (!t?.ok || !t.branch || !t.repo || !t.path || !Number.isInteger(t.issue)) {
  const reason = t?.error || 'pr_target.py 沒有回報完整的 branch、repo、path、issue'
  log(`${tag} 準備失敗：${reason}`)
  return { pr, ci_pass: false, pushed: false, summary: '', error: `準備：${reason}` }
}
log(`${tag} 分支 ${t.branch}，issue #${t.issue}${t.created ? '，新建 worktree' : ''}`)

// ───────────────── 修改：改檔 → 驗證 → commit → push → 等 CI ─────────────────
const S = `${t.repo}/script/workflow`
const RULES = `硬性規則（違反就算失敗）：
- 只動 worktree ${t.path}。不碰主 repo ${t.repo}：不在那裡改檔、不 pull、不動它的未追蹤檔。
- 不 merge、不開新 PR、不改 PR 本文。要留言的話自己逐一下 gh 指令並帶 \`-R ${SLUG}\`，不要包進腳本或用 && 串。
- 只改這次要修的問題；不要順手改別的東西。內容不准有本機絕對路徑。
- commit 剛好一個，照 repo 格式；不加 Claude 署名、Co-Authored-By 或 session 連結。
- 只准 push 到 ${t.branch}，一般 push；不准 push main、不准 force push main。只有需要 rebase（PR 跟 main 衝突，或 push 被拒且原因是跟 origin/main 衝突）時才 \`git -C ${t.path} fetch origin\`、\`git -C ${t.path} rebase origin/main\`，再 \`git -C ${t.path} push --force-with-lease origin ${t.branch}\`，只限這個分支。
- 機械步驟用 ${S}/ 的腳本，讀它輸出的 JSON 判斷成敗，不要自己重寫一遍。
- 子代理自己判斷的只有兩件事：怎麼修改，以及驗證失敗時要修還是停下。其他步驟照順序做，任何一步失敗就停下回報。`

const RES = {
  type: 'object',
  properties: {
    ci_pass: { type: 'boolean' },
    pushed: { type: 'boolean' },
    commit: { type: 'string' },
    summary: { type: 'string' },
    error: { type: 'string' },
  },
  required: ['ci_pass', 'pushed', 'summary'],
}

phase('修改')
const r = await agent(`${tag} 修改：在 worktree ${t.path}（PR ${SLUG}#${pr}，分支 ${t.branch}，issue #${t.issue}）修一個問題。worktree 已確認乾淨且在 PR 分支最新${t.behind_main ? `，落後 origin/main ${t.behind_main} 個 commit` : ''}。

問題：${problem}

要做：${todo}

${RULES}

步驟（照順序）：
1. 修改：照「要做」在 ${t.path} 裡改。
2. 驗證：\`python3 ${S}/verify.py --root ${t.path}\`。它跑 docs.yml 每個 \`run:\`、每個 \`script/*/test\` 的 unittest、check_script_layout、hooks 的守門測試（hooks 的測試由 \`.claude/hooks/test\` 跑），並檢查每個 \`script/*/test\` 都在 docs.yml 裡；ok 是 true 才算過。失敗時看 steps 裡 ok 是 false 的 output 自己判斷：是這次改動造成的就修好再重跑一次 verify.py；修不了或跟這次無關就停下，不要 commit，在 error 寫清楚。
3. commit 一個：\`git -C ${t.path} add\` 這次改的檔，再 \`git -C ${t.path} commit -m "${q(commit)}" -m "Refs: #${t.issue}"\`。
4. push：\`git -C ${t.path} push origin ${t.branch}\`。
5. 等 CI：\`python3 ${S}/wait_ci.py ${pr}\`（預設最多 600 秒）。結束碼 0＝全過；1＝有失敗：看 \`gh run view --log-failed -R ${SLUG}\`，是這次改動造成的就修，再 commit（同樣格式、footer \`Refs: #${t.issue}\`）、push、再等一次，修不了就停；2＝逾時，停下回報。CI 全過就停，不 merge。

回報：ci_pass（最後一次 wait_ci 是否全過）、pushed（有沒有 push 成功）、commit（最後一個 commit 的 hash）、summary（改了什麼、驗證結果、特別處理例如 rebase）、error（失敗時寫停在哪一步、為什麼）。`, { label: `${tag} 修改`, phase: '修改', schema: RES })

log(`${tag} ${r?.ci_pass ? 'CI 全過' : `沒有完成：${r?.error || 'CI 沒有全過'}`}`)

return {
  pr,
  branch: t.branch,
  issue: t.issue,
  url: t.url,
  ci_pass: !!r?.ci_pass,
  pushed: !!r?.pushed,
  commit: r?.commit,
  summary: r?.summary ?? '',
  error: r?.error,
}

// ───────────────── args 範例（可直接貼進 Workflow 的 args） ─────────────────
// {
//   "pr": 175,
//   "problem": ".claude/hooks/monitor_guard.py 的擋下訊息寫了本機絕對路徑，repo 內容不准有本機絕對路徑。",
//   "todo": "訊息改成 repo 相對路徑（在 repo 根目錄執行 sh script/github/watch_github.sh 60 --once）；.claude/hooks/test/test_monitor_guard.py 有檢查訊息內容就同步。",
//   "commit": "fix(hooks): monitor_guard 提示改用 repo 相對路徑"
// }
