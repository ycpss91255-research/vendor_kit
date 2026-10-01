export const meta = {
  name: 'research',
  description: 'agy 查 → codex 核對 → Claude 整合 → 貼 issue',
  whenToUse: '要找外部前例或資料當決策依據時（例如大型 repo 怎麼設定某件事）；brief 先寫好放在 workspace 的 reference/research/<issue>/',
  phases: [
    { title: '調查', detail: '每個 brief 一個 agy；輸出已存在且非空就沿用' },
    { title: '核對', detail: '每份 agy 輸出交給 codex，逐條打開來源核對，標正確／有誤／查不到' },
    { title: '整合', detail: 'Claude 讀全部 agy 與 codex 輸出，抽查來源，寫整合結論；兩方不一致列成分歧，不選邊' },
    { title: '貼 issue', detail: '依序貼 [agy] 原文、[codex] 原文、[claude] 整合結論' },
  ],
}

// args:
//   issue      number  必填，結果貼到這個 issue
//   topic      string  必填，一句話說明調查目的（給 codex 與 Claude 的背景）
//   briefs     array   必填，每項 { id, label }：brief 檔是 <dir>/<id>_brief.md，agy 輸出 <dir>/<id>_agy.md
//   dir        string  可省，預設 /home/cyc/Desktop/vendor-kit_ws/reference/research/<issue>（不放 /tmp）
//   background string  可省，已定案前提
//   post       boolean 可省，預設 true；false 就只產檔不貼 issue
const { issue, topic, briefs, background = '', post = true } = args ?? {}
if (!Number.isInteger(issue)) throw new Error('args.issue 必填（issue 編號）')
if (typeof topic !== 'string' || !topic.trim()) throw new Error('args.topic 必填')
if (!Array.isArray(briefs) || briefs.length === 0) throw new Error('args.briefs 必填')
log(`research #${issue}`)
const dir = args.dir ?? `/home/cyc/Desktop/vendor-kit_ws/reference/research/${issue}`
const REPO = 'ycpss91255-research/vendor_kit'
const BG = background.trim() ? `已定案前提（不要質疑）：\n${background.trim()}\n` : ''
const brief = b => `${dir}/${b.id}_brief.md`
const agyOut = b => `${dir}/${b.id}_agy.md`
const codexOut = b => `${dir}/${b.id}_codex.md`
const claudeOut = `${dir}/claude_review.md`

const RUN = {
  type: 'object',
  properties: { exit: { type: 'integer' }, out_ok: { type: 'boolean' }, reused: { type: 'boolean' }, error: { type: 'string' } },
  required: ['exit', 'out_ok'],
}

const results = await pipeline(
  briefs,
  b => agent(`你的工作是執行 agy 做資料調查，**你自己不調查、不改寫輸出**。不改任何 repo、不 commit、不 push。

1. ${agyOut(b)} 已存在而且非空：不重跑，回報 reused=true、exit=0、out_ok=true。
2. 否則前景執行（Bash timeout 600000；跑不完就改用 run_in_background 並等它結束，不要中途放棄）：
   \`cd ${dir} && agy -p "$(cat ${brief(b)})" > ${agyOut(b)} 2> ${dir}/${b.id}_agy.err; echo "agy_exit=$?"\`
3. 回報 exit（agy_exit 的值）、out_ok（輸出檔存在且非空）；失敗把 ${dir}/${b.id}_agy.err 的內容寫進 error。結束後刪掉空的 .err 檔。`,
    { label: `#${issue} agy:${b.id}`, phase: '調查', schema: RUN }),
  (r, b) => {
    if (!r || r.exit !== 0 || !r.out_ok) return { b, agy: r, codex: null }
    return agent(`你的工作是啟動 codex 核對 agy 的調查結果，**你自己不核對、不加意見**。不改任何 repo、不 commit、不 push。

1. 用 heredoc（'EOF'）把下面的 brief 原文寫進 ${dir}/${b.id}_codex_brief.md：
---
${BG}調查目的：${topic}
讀 ${agyOut(b)}（agy 的調查輸出）與它的題目 ${brief(b)}。逐條打開 agy 引用的來源（網址、workflow 檔、文件）核對：每條標「正確／有誤／查不到來源」，有誤就寫出正確內容與來源網址。agy 漏掉的重要事實自己補上，同樣附來源。最後一節「核對後結論」：依核對結果修正後的結論與數量統計。用繁體中文 markdown，不要改任何檔。
---
2. 前景執行（Bash timeout 600000），形狀一字不差：
   \`bash -c 'codex exec --skip-git-repo-check -C ${dir} -o ${codexOut(b)} "$(cat ${dir}/${b.id}_codex_brief.md)" < /dev/null; echo "codex_exit=$?"'\`
3. 回報 exit（codex_exit 的值）、out_ok（${codexOut(b)} 存在且非空）。結束後刪掉 ${dir}/${b.id}_codex_brief.md。`,
      { label: `#${issue} codex:${b.id}`, phase: '核對', schema: RUN }).then(c => ({ b, agy: r, codex: c }))
  },
)

const ok = results.filter(x => x && x.codex && x.codex.exit === 0 && x.codex.out_ok)
const failed = results.filter(x => !ok.includes(x)).map(x => ({ id: x?.b?.id, agy: x?.agy, codex: x?.codex }))
if (failed.length) log(`未完成：${failed.map(f => f.id).join('、')}`)
if (!ok.length) return { failed }

phase('整合')
const review = await agent(`你負責整合外部調查的結果。不改任何 repo、不 commit、不 push、不發 issue。

${BG}調查目的：${topic}
資料（每組是 agy 調查與 codex 核對）：
${ok.map(x => `- ${x.b.label}：${agyOut(x.b)}、${codexOut(x.b)}`).join('\n')}

做法：
1. 兩份都讀。codex 標「有誤」或兩者說法不同的地方，自己打開來源抽查（WebFetch），以來源為準。
2. 寫整合結論：每組的主流做法與數量（以核對後的結果為準），各自附代表 repo 與來源連結；組與組之間的差異；對「調查目的」的意涵。
3. agy、codex 與你的判斷不一致、而來源無法判定的，列在「分歧」一節，各方立場都寫，不替任何一方下定論。
4. 沒有來源的主張標明是推論。

用繁體中文 markdown 寫到 ${claudeOut}，回報 output_file 與 summary（結論一節的全文）。`,
  { label: `#${issue} Claude 整合`, phase: '整合', schema: { type: 'object', properties: { output_file: { type: 'string' }, summary: { type: 'string' }, error: { type: 'string' } }, required: ['output_file', 'summary'] } })

if (!post || !review) return { ok: ok.map(x => x.b.id), failed, review }

phase('貼 issue')
const posted = await agent(`把調查結果依序貼到 GitHub issue #${issue}（repo ${REPO}）。不改 repo、不 commit。

規則：
- 每則留言先寫成檔，再用另一個指令 \`gh issue comment ${issue} -R ${REPO} --body-file <絕對路徑>\` 貼出；不要用變數代替路徑，也不要在同一個指令裡寫檔。
- 本文第一行一律是標記：agy 原文用 \`[agy] \`、codex 原文用 \`[codex] \`、整合結論用 \`[claude] \`。[agy]、[codex] 只能貼原文，不准改寫；第二行加一行「（註：…）」說明這是哪一份 brief 的輸出原文、未改寫。
- 本文不准出現本機絕對路徑（/home/…、/tmp/…）：原文若有，就在註記行說明並把該路徑換成相對於 workspace 的寫法（例如 reference/research/${issue}/…），其他字不動。
- 單則超過 60000 字元就切成幾則，標「（1/2）」這類序號。
- 留言檔寫在 ${dir}/post_*.md，貼完刪掉。

順序：
${ok.map(x => `1. [agy] ${x.b.label}：${agyOut(x.b)}\n2. [codex] ${x.b.label} 的核對：${codexOut(x.b)}`).join('\n')}
最後. [claude] 整合結論：${claudeOut}

回報每則留言的網址。`,
  { label: `#${issue} 貼 issue`, phase: '貼 issue', schema: { type: 'object', properties: { urls: { type: 'array', items: { type: 'string' } }, error: { type: 'string' } }, required: ['urls'] } })

return { ok: ok.map(x => x.b.id), failed, summary: review.summary, urls: posted?.urls ?? [] }
