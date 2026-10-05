export const meta = {
  name: 'pr-fix',
  description: '在已開 PR 的 worktree 修問題：準備 worktree → 修改 → 驗證 → 一個 commit → push → 等 CI；不 merge。pr 給陣列時各 PR 同時修、互不影響',
  whenToUse: 'PR 已經開了、CI 或審查要求再改時；每個 PR 一次修一個問題，CI 通過就停；好幾個 PR 要同時修（例如一起 rebase）時給 pr 陣列',
  phases: [
    { title: '準備', detail: 'pr_target.py 查分支、worktree、issue，並確認 worktree 乾淨且在 PR 分支最新' },
    { title: '修改', detail: '子代理在 worktree 修改；verify.py 跑全部驗證；commit_push.py commit 並 push；wait_ci.py --failed-logs 等 CI' },
  ],
}

// args: {
//   pr: number | number[],              // 必填，PR 編號或編號陣列；陣列時各 PR 同時修，一個失敗不影響其他。分支、worktree、issue 由 script/workflow/pr_target.py 查
//   problem: string | { [pr]: string }, // 必填，要修的問題；字串＝所有 PR 共用，物件＝以 PR 編號為鍵各自給
//   todo: string | { [pr]: string },    // 必填，要做的事（給子代理的任務描述）；共用或各自給，同上
//   commit: string | { [pr]: string },  // 必填，commit 訊息第一行（type(scope): 摘要）；共用或各自給，同上。footer 由 workflow 補 Refs: #<issue>
//   repoRoot?: string,                  // 主 repo；不給就用子代理的工作目錄（主 repo 根目錄），由 pr_target.py 回報實際位置
// }
const {
  pr,
  problem,
  todo,
  commit,
  repoRoot,
} = args ?? {}

// ───────────────── 參數檢查 ─────────────────
const many = Array.isArray(pr)
const prs = many ? pr : [pr]
if (!prs.length || !prs.every(n => Number.isInteger(n) && n > 0)) {
  throw new Error('args.pr 必填：PR 編號（正整數）或編號陣列')
}
const dupPrs = [...new Set(prs.filter((n, i) => prs.indexOf(n) !== i))]
if (dupPrs.length) {
  throw new Error(`args.pr 不能重複：${dupPrs.join('、')}`)
}
const FIELDS = { problem, todo, commit }
const isMap = v => v !== null && typeof v === 'object' && !Array.isArray(v)
for (const [k, v] of Object.entries(FIELDS)) {
  if (!isMap(v)) continue
  const extra = Object.keys(v).filter(key => !prs.includes(Number(key)))
  if (extra.length) {
    throw new Error(`args.${k} 的鍵要是 args.pr 裡的 PR 編號；多了 ${extra.join('、')}`)
  }
}
// 取某個 PR 的欄位值：字串＝共用，物件＝以 PR 編號為鍵
const pick = (v, n) => (isMap(v) ? v[String(n)] : v)
const missing = []
for (const n of prs) {
  for (const [k, v] of Object.entries(FIELDS)) {
    const x = pick(v, n)
    if (typeof x !== 'string' || !x.trim()) missing.push(many ? `${k}[${n}]` : k)
  }
}
if (missing.length) {
  throw new Error(`args 缺必填欄位：${missing.join('、')}（problem＝要修的問題、todo＝要做的事、commit＝commit 訊息第一行；可以是字串（共用）或以 PR 編號為鍵的物件）`)
}
const multiline = prs.filter(n => pick(commit, n).includes('\n'))
if (multiline.length) {
  throw new Error(`args.commit 只放 commit 訊息第一行（type(scope): 摘要）；footer Refs: #<issue> 由 workflow 補${many ? `（PR ${multiline.join('、')}）` : ''}`)
}

const SLUG = 'ycpss91255-research/vendor_kit'
log(`pr-fix ${prs.map(n => `#${n}`).join(' ')}${many ? '（並行）' : ''}`)

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

// 修一個 PR：準備 → 修改；回傳這個 PR 的結果
async function fixOne(n) {
  const tag = `#${n}`
  const problemN = pick(problem, n)
  const todoN = pick(todo, n)
  const commitN = pick(commit, n)
  // 並行的子代理共用同一個 scratchpad：固定檔名會互相覆蓋（#241），所以暫存檔一律放以 PR 編號命名的子目錄
  const tmp = `<你的 scratchpad>/pr-fix/${n}`
  const TMP_RULE = `- 暫存檔（commit 訊息、留言本文、一次性腳本、輸出紀錄）一律放 ${tmp}/（先 mkdir -p），不要放 scratchpad 根目錄，也不要用別的子代理也可能用的檔名；同時可能有其他 PR 的子代理在跑。`

  // ───────────────── 準備：查分支、worktree、issue ─────────────────
  const prep = repoRoot
    ? `python3 ${repoRoot}/script/workflow/pr_target.py ${n} --repo ${repoRoot}`
    : `python3 script/workflow/pr_target.py ${n}`
  const t = await agent(`${tag} 準備：只跑一個指令，不要改任何檔。${repoRoot ? '' : '在你的工作目錄（主 repo 根目錄）執行。'}

\`${prep}\`

它會用唯讀的 \`gh pr view\` 查 PR 分支與本文、從本文取第一個 Closes／Refs #N 當 issue、在 worktree/branch/<分支> 找或建 worktree，並確認 worktree 乾淨、在 PR 分支最新（落後就 fast-forward）。同時有別的 pr_target.py 在跑時，它會在主 repo 的鎖上排隊，等一下是正常的。
把它輸出的那一行 JSON 原樣照欄位回報（ok、branch、issue、repo、path、url、created、behind_main、error）。ok 是 false 就照抄 error，不要自己補救、不要重試別的寫法。`, { label: `${tag} 準備`, phase: '準備', schema: TARGET })

  if (!t?.ok || !t.branch || !t.repo || !t.path || !Number.isInteger(t.issue)) {
    const reason = t?.error || 'pr_target.py 沒有回報完整的 branch、repo、path、issue'
    log(`${tag} 準備失敗：${reason}`)
    return { pr: n, ci_pass: false, pushed: false, summary: '', error: `準備：${reason}` }
  }
  log(`${tag} 分支 ${t.branch}，issue #${t.issue}${t.created ? '，新建 worktree' : ''}`)

  // ───────────────── 修改：改檔 → 驗證 → commit → push → 等 CI ─────────────────
  // 腳本一律從主 repo 的 script/ 取：worktree 的分支可能還沒有這些腳本
  const S = `${t.repo}/script/workflow`
  const G = `${t.repo}/script/git`
  const H = `${t.repo}/script/github`
  const MSG = `${tmp}/commit-msg.txt`
  const RULES = `硬性規則（違反就算失敗）：
- 只動 worktree ${t.path}。不碰主 repo ${t.repo}：不在那裡改檔、不 pull、不動它的未追蹤檔。
- 不 merge、不開新 PR、不改 PR 本文。要留言的話本文先寫成檔（第一行 \`[claude]\` 開頭），再跑 \`python3 ${H}/post_comments.py --kind pr --number ${n} --body-file <檔>\`，讀它的 JSON 判斷成敗；不要自己下 \`gh pr comment\`。
- 只改這次要修的問題；不要順手改別的東西。內容不准有本機絕對路徑。
- commit 剛好一個，照 repo 格式；不加 Claude 署名、Co-Authored-By 或 session 連結。
- 只准 push 到 ${t.branch}；不准 push main、不准 force push main。push 只經 \`${G}/commit_push.py\` 與 \`${G}/rebase_push.py\`，不自己下 \`git push\`。只有需要 rebase（PR 跟 main 衝突，或 push 被拒且原因是跟 origin/main 衝突）時才跑 \`python3 ${G}/rebase_push.py --repo ${t.path} --branch ${t.branch}\`（fetch、rebase origin/main、\`--force-with-lease\` 推回這個分支）；JSON 的 state 是 conflict 時照 conflicts 解衝突（這是要判斷的），\`git -C ${t.path} add\` 解好的檔後跑同一行加 \`--continue\`，直到 state 是 rebased 或 up_to_date；ok 是 false 就停下回報。
${TMP_RULE}
- 機械步驟用 ${S}/ 的腳本，讀它輸出的 JSON 判斷成敗，不要自己重寫一遍。
- 子代理自己判斷的只有兩件事：怎麼修改，以及驗證失敗時要修還是停下。其他步驟照順序做，任何一步失敗就停下回報。`

  const r = await agent(`${tag} 修改：在 worktree ${t.path}（PR ${SLUG}#${n}，分支 ${t.branch}，issue #${t.issue}）修一個問題。worktree 已確認乾淨且在 PR 分支最新${t.behind_main ? `，落後 origin/main ${t.behind_main} 個 commit` : ''}。

問題：${problemN}

要做：${todoN}

${RULES}

步驟（照順序）：
1. 修改：照「要做」在 ${t.path} 裡改。
2. 驗證：\`python3 ${S}/verify.py --root ${t.path}\`。它跑 docs.yml 每個 \`run:\`、每個 \`script/*/test\` 的 unittest、check_script_layout、hooks 的守門測試（hooks 的測試由 \`.claude/hooks/test\` 跑），並檢查每個 \`script/*/test\` 都在 docs.yml 裡；ok 是 true 才算過。失敗時看 steps 裡 ok 是 false 的 output 自己判斷：是這次改動造成的就修好再重跑一次 verify.py；修不了或跟這次無關就停下，不要 commit，在 error 寫清楚。
3. commit 一個並 push：用 Write 工具把下面這一行（commit 訊息第一行，不含 footer）原樣寫成檔 ${MSG}：

${commitN}

再跑 \`python3 ${G}/commit_push.py --repo ${t.path} --branch ${t.branch} --message-file ${MSG} --refs ${t.issue} --all\`。它檢查訊息、補 footer \`Refs: #${t.issue}\`、\`git add -A\`、commit、push 到 ${t.branch}，每個寫入前都經 hook 檢查。讀它的 JSON：ok 是 true 才算 commit 與 push 成功，commit 回報 JSON 的 commit，pushed 回報 JSON 的 pushed；ok 是 false 就照 step、problems、denied、error 停下回報，不要自己改用 git commit／git push 補做。
4. 等 CI：\`python3 ${S}/wait_ci.py ${n} --failed-logs\`（預設最多 600 秒）。結束碼 0＝全過；1＝有失敗：看 JSON 的 failed_logs（每個失敗 check 的日誌尾段 tail；tail 是 null 時看 error），是這次改動造成的就修，修好後重跑一次 verify.py，再照第 3 步用同一個訊息檔跑同一行 commit_push.py，再等一次，修不了就停；2＝逾時，停下回報。CI 全過就停，不 merge。

回報：ci_pass（最後一次 wait_ci 是否全過）、pushed（有沒有 push 成功）、commit（最後一次 commit_push.py JSON 的 commit）、summary（改了什麼、驗證結果、特別處理例如 rebase）、error（失敗時寫停在哪一步、為什麼）。`, { label: `${tag} 修改`, phase: '修改', schema: RES })

  log(`${tag} ${r?.ci_pass ? 'CI 全過' : `沒有完成：${r?.error || 'CI 沒有全過'}`}`)

  return {
    pr: n,
    branch: t.branch,
    issue: t.issue,
    url: t.url,
    ci_pass: !!r?.ci_pass,
    pushed: !!r?.pushed,
    commit: r?.commit,
    summary: r?.summary ?? '',
    error: r?.error,
  }
}

// ───────────────── 執行：單一 PR 回傳一個結果；陣列時同時修、互不影響 ─────────────────
if (!many) {
  return await fixOne(prs[0])
}

// 各 PR 獨立：一個 PR 的子代理失敗或丟錯，只記在它自己的結果，不影響其他 PR
const results = await parallel(prs.map(n => async () => {
  try {
    return await fixOne(n)
  } catch (e) {
    return { pr: n, ci_pass: false, pushed: false, summary: '', error: `子代理失敗：${e?.message ?? e}` }
  }
}))
const failed = results.filter(o => !o?.ci_pass).map(o => ({ pr: o.pr, reason: o.error || 'CI 沒有全過' }))
log(`完成：${results.length - failed.length}/${prs.length} 個 PR${failed.length ? `，沒有完成 ${failed.map(f => `#${f.pr}`).join(' ')}` : ''}`)

return { prs, results, failed }

// ───────────────── args 範例（可直接貼進 Workflow 的 args） ─────────────────
// 單一 PR：
// {
//   "pr": 175,
//   "problem": ".claude/hooks/monitor_guard.py 的擋下訊息寫了本機絕對路徑，repo 內容不准有本機絕對路徑。",
//   "todo": "訊息改成 repo 相對路徑（在 repo 根目錄執行 sh script/github/watch_github.sh 60 --once）；.claude/hooks/test/test_monitor_guard.py 有檢查訊息內容就同步。",
//   "commit": "fix(hooks): monitor_guard 提示改用 repo 相對路徑"
// }
// 多個 PR（todo 共用，problem、commit 各自給）：
// {
//   "pr": [234, 235],
//   "problem": {
//     "234": "verify.py 的說明還寫舊的 test_guard.py 位置。",
//     "235": "pr workflow 的驗證說明還寫舊的 test_guard.py 位置。"
//   },
//   "todo": "說明改成不綁 test_guard.py 的位置，只寫 hooks 的測試由 .claude/hooks/test 跑。",
//   "commit": {
//     "234": "docs(workflow): verify.py 說明不綁 test_guard.py 位置",
//     "235": "docs(workflow): pr 的驗證說明不綁 test_guard.py 位置"
//   }
// }
