"""三階段 draw.io 審查工具鏈 ─ 第 2 步：機械 lint。
用法: python3 lint_pages.py <outdir>            （<outdir> = extract_pages.py 的輸出目錄）
輸出 <outdir>/lint.md（依頁分組，每條含 id、規則代號、等級 warn/info）與 <outdir>/lint.json（同內容，機器用）。

規則（代號）：
  dangling   懸空：流程頁（頁名符合 FLOW_PAGE_RE）上 step／decision 要有進邊＋出邊；end_* 只需進邊（綠橢圓沒進邊但有出邊 = 起點，不報）；
             entry 只需出邊；IMG（紫 image 框）至少一條線（info）。非流程頁略過（info 一行）。
  decision   判斷菱形出邊數 ≠ 2（warn）；出邊標籤不以「是」「否」開頭（info；「失敗」「成功」「是：…」「否 →…」都算列出）；兩條出邊標籤相同（warn）。
  endcolor   終點顏色 vs 文字：含「→ 0」「0：」但不是綠（warn）；含「→ 1／2／3」或以「1：／2：／3：」開頭但是綠（warn）；
             含「請」「先」「手動」「重跑」「解決」而是紅（info：候選改橙）。
  xref       文字引用的頁名在頁名清單找不到（warn）；只靠拆字模糊比對到（info）。
  term-diff  跨頁：同一名詞 name 在不同頁 text 不一致 → 列版本與差異摘要（放在最後「跨頁」段；warn）。
  base       文字出現 \\bbase\\b（排除 BASE_ALLOW 內的片語；warn）。
  color      頁內 fillColor 不在該頁圖例（warn；白／none 不算）；沒有圖例的頁 info。
  termcov    名詞覆蓋：node 文字出現 KEYWORDS 的關鍵字，名詞表沒有對應條：名詞 name 或 text 含 → 過（text-only 的只彙總成一行 info）；都沒有 → warn。
  onething   一格一事候選：step／end 節點文字中「→」「並」「然後」「再」「、」「；」總數 ≥ 2 → info（交第 3 階段代理判定）。

v2 新增（每條可在 ENABLED 關閉；等級都是 warn）：
  event-name      node／edge 文字出現 launcher_started|…|_completed 等舊事件名 → 「事件名須用 spec 註冊表：launcher_start/exit、engine_start/exit」。
  resolve-3way    流程頁上文字含「docker run」且含「resolve」的 step：沿出邊走（藍 SUB／file／note 不計步；「續「X」頁」出口會接到 X 頁的「來自」入口）
                  ≤ RESOLVE_3WAY_DEPTH 步內，須同時有 (A) decision 文字含「回 0」「結束碼 0」「非 0」，(B) 另一個 decision／step 文字含「6-30」或「文法」（A≠B）。
  precheck-recover 頁名含 install|add|remove|upgrade|dev|undev|uninstall|升引擎 的第一頁（頁名含「（1）」或不含全形括號，且頁上有起點綠橢圓）
                  須有 decision 文字含「未完成」「既有進度檔」「恢復」；頁名含 sync|update 的第一頁須有節點文字含「6-33」；prune 頁只要有「只列出」。
  end-color-text  end 節點：文字含「→ 0」或以「0：」開頭 → 須 end_ok；含 6-24|6-31|6-38|6-30|寫不進|拉不到 → 須 end_red；
                  含 請|先 |手動|重跑|→ 3|6-4|6-33 且不含紅關鍵字 → 須 end_orange（舊 endcolor 保留）。
  xref-forward    xrefs 指到的頁序號（頁名前綴數字；沒有就用 pages.json 順序）大於本頁 → 「前引」；「續「X」頁」出口允許向後，排除。
  write-line      step 文字（去掉「是：」「否 →」前綴後）以 寫|建|刪|原子替換|append 開頭或含「→ 檔」，頁內有 file 節點，但沒有出邊指到 file 節點。
                  例外詞 WRITE_LINE_EXEMPT（印、印出…；「印記」只在「寫印記」時算寫入）。
  write-fail-edge 同上寫入 step：必須有一條「可見」出邊滿足其一：target 是 end_red／end_orange、target 文字含「失敗匯流」、label 含「失敗」；
                  否則 warn（第十七輪起不再靠「頁內有任一步／失敗匯流節點」豁免；隱形邊不算）。
  hidden-edge     頁內有 visible="0" 的隱形邊（extract 標 hidden）→ warn；lint 的其他規則一律視隱形邊為不存在。
  term-count      名詞表條數 > TERM_MAX。 term-dup-page0：名詞 name 已在第 0 頁（PAGE0_IDS 的 terms）出現。
  page-height     max(y+h) > PAGE_MAX_H。 edge-font：edge fontSize 存在且 ≠ EDGE_FONT。審閱頁 REVIEW_PAGE_IDS 豁免 term-count 與 page-height。
  merge-fanout    step 出邊 ≥ 3 且 targets 全是 end_* → 「終點扇出：分支來源不可辨」。
"""
import re, json, os, sys, glob, difflib
from collections import defaultdict, Counter

# ---------- 可調參數 ----------
FLOW_PAGE_RE = re.compile(r'^(?:\d+ )?(流程|狀態機)')   # 頁名可帶序號前綴「NN 」
KEYWORDS = [                      # (顯示名, regex)。名詞表的 name 或 text 含到 regex 命中的原字串就算覆蓋
    ('訊息碼 6-xx', r'\b6-\d+[a-z]?\b'),
    ('.tmp.*', r'\.tmp\.[A-Za-z_]+'),
    ('gen/…', r'\bgen/[\w.]*'),
    ('version.local.toml', r'version\.local\.toml'),
    ('version.toml', r'(?<!local\.)\bversion\.toml'),
    ('config.toml', r'config\.toml'),
    ('log/', r'\blog/'),
    ('baseline/', r'baseline/'),
    ('cache/', r'\bcache/'),
    ('metadata', r'metadata'),
    ('frozen', r'\bfrozen\b'),
    ('flock', r'\bflock\b'),
    ('digest', r'\bdigest\b'),
    ('--local', r'--local\b'),
    ('resolve／apply', r'\b(resolve|apply)\b'),
    ('Renovate', r'\bRenovate\b'),
    ('薄殼', r'薄殼'),
    ('進度日誌', r'進度日誌'),
]
BASE_ALLOW = ['對齊 base 的 just 慣例', 'test-base', 'base_raw', 'base_ref']   # 這些片語裡的 base 不算實例
COLOR_WHITELIST = {'#ffffff', 'none', '-', ''}
ONETHING_TOKENS = ['→', '並', '然後', '再', '、', '；']
ONETHING_MIN = 2
YESNO_RE = re.compile(r'^(是|否)')
NEEDS_HUMAN = ['請', '先', '手動', '重跑', '解決']

# ---------- v2 新規則的開關與參數 ----------
HIDDEN_EDGE = True   # 隱形邊（visible=0）視為不存在；並另報 hidden-edge warn
ENABLED = {                       # False = 關掉該條
    'event-name': True, 'resolve-3way': True, 'precheck-recover': True, 'end-color-text': True, 'xref-forward': True,
    'write-line': True, 'write-fail-edge': True, 'term-count': True, 'term-dup-page0': True,
    'page-height': True, 'edge-font': True, 'merge-fanout': True, 'hidden-edge': True,
}
EVENT_NAME_RE = re.compile(r'launcher_started|launcher_completed|launcher_failed|engine_started|engine_completed|engine_failed|_started\b|_completed\b')
RESOLVE_3WAY_DEPTH = 3            # 從「docker run … resolve」格往下走幾步（只算啟動器的白 step；藍 SUB、菱形、file、note、entry 不計步 ── 引擎內的判斷菱形沒有樣式可分，故一律不計）
RESOLVE_3WAY_CROSS_PAGE = True    # 走到「續「X」頁」出口時接到 X 頁的「來自」入口續走
RESOLVE_STEP_RE = re.compile(r'docker run\b[^（()⏎]*?\bresolve\b')   # 「docker run … resolve」且中間沒有括號（排除 apply 格的「（含 vk-resolve）」與括號內的順帶提及）
RESOLVE_EXIT_RE = re.compile(r'回 ?0|結束碼 ?0|非 ?0')
RESOLVE_GRAMMAR_RE = re.compile(r'6-30|文法')
PRECHECK_VERB_RE = re.compile(r'install|add|remove|upgrade|dev|undev|uninstall|升引擎')
PRECHECK_SYNC_RE = re.compile(r'sync|update')
PRECHECK_DECISION_RE = re.compile(r'未完成|既有進度檔|恢復')
PRECHECK_FIRST_RE = re.compile(r'（1）')            # 頁名含這個 = 第一頁；或頁名完全不含全形括號。另外：頁上有「來自「X」頁」入口的 = 續頁，不查
PRECHECK_SKIP_RE = re.compile(r'回退')                             # 例：re.compile(r'回退')；頁名符合就不查（預設不跳過）
END_OK_RE = re.compile(r'→\s*0\b|^0：')
END_RED_RE = re.compile(r'6-24|6-31|6-38|6-30|寫不進|拉不到|寫入失敗|失敗（任一步）')
END_ORANGE_RE = re.compile(r'請|先 |手動|重跑|→\s*3\b|6-4\b|6-33')
WRITE_PREFIX_RE = re.compile(r'^(?:(?:是|否|有|無|缺|失敗|成功)\s*[:：→]\s*)+')   # 去掉「是：」「否 →」等分支前綴再判斷
WRITE_VERB_RE = re.compile(r'^(寫|建|刪|原子替換|append\b)|→ 檔')
WRITE_PAGE_RE = re.compile(r'^(?:\d+ )?流程(?!.*release)')     # write-line／write-fail-edge 只查流程頁（狀態機頁的格是狀態，不是寫入步驟）
WRITE_LINE_EXEMPT = ['印出', '印記', '印', '執行紀錄', 'launcher_', 'engine_', 'sync_fast_path']   # 寫入動詞後緊接這些詞就不算寫檔（「寫印記」例外，仍算；執行紀錄／事件 = 圖例約定隱含，不畫 log/ 框）
WRITE_LINE_EXEMPT_ANY = ['到暫存', '暫存副本']      # 文字含這些 = 寫到暫存（不是專案裡的檔），不算
WRITE_LINE_FORCE = ['寫印記']                      # 以這些開頭一定算寫入
WRITE_FAIL_HUB_RE = re.compile(r'失敗匯流')   # write-fail-edge：可見出邊的 target 文字含此 = 進了失敗匯流格
TERM_MAX = 8
PAGE0_IDS = ['v1p0']
REVIEW_PAGE_IDS = ['v1p0', 'v1p1', 'v1p1i']
PAGE_MAX_H = 2400
EDGE_FONT = '12'
MERGE_FANOUT_MIN = 3

def load_pages(outdir):
    """依 pages.json（文件內頁序）讀每頁 JSON；沒有 pages.json 就照檔名。"""
    pj = os.path.join(outdir, 'pages.json')
    if os.path.exists(pj):
        names = json.load(open(pj, encoding='utf-8'))
        files = [os.path.join(outdir, f"{p['id']}.json") for p in names]
    else:
        files = sorted(glob.glob(os.path.join(outdir, 'v*.json'))); names = None
    pages = [json.load(open(f, encoding='utf-8')) for f in files if os.path.exists(f)]
    if names is None: names = [p['page'] for p in pages]
    return pages, names

def norm(s): return re.sub(r'\s+', '', s)

def xref_ok(ref, page_names):
    """回傳 'exact' / 'fuzzy' / None。exact = 頁名包含引用（去空白）；
    fuzzy = 把引用拆成 token（英數字串／CJK 連續字），某頁名全部包含，例如「B（1′）」對到「B. 手動路徑（1′）apply 前置」；
    「X（1）（2）」／「E(a)(b)」這種多括號引用展開成多個，每個都要找得到。"""
    r = norm(ref); names = [norm(n) for n in page_names]
    if any(r in n for n in names): return 'exact'
    parens = re.findall(r'[（(][^（）()]*[）)]', r)
    if len(parens) > 1:
        head = re.sub(r'[（(][^（）()]*[）)]', '', r)
        res = [xref_ok(head + p, page_names) for p in parens]
        return None if any(x is None for x in res) else 'fuzzy'
    toks = re.findall(r"[A-Za-z0-9′.\-]+|[\u4e00-\u9fff]+", r)
    if toks and any(all(t in n for t in toks) for n in names): return 'fuzzy'
    return None

def page_seq(name, idx):
    """頁序號：頁名前綴數字；沒有就用 pages.json 的順序（1 起）。"""
    m = re.match(r'\s*(\d+)\s', name)
    return int(m.group(1)) if m else idx + 1

def xref_targets(ref, page_names):
    """引用 → 命中的頁名 index 清單（exact 優先，沒有才 fuzzy；多括號引用展開）。"""
    r = norm(ref); names = [norm(n) for n in page_names]
    hit = [i for i, n in enumerate(names) if r in n]
    if hit: return hit
    parens = re.findall(r'[（(][^（）()]*[）)]', r)
    if len(parens) > 1:
        head = re.sub(r'[（(][^（）()]*[）)]', '', r); res = []
        for p in parens: res += xref_targets(head + p, page_names)
        return res
    toks = re.findall(r"[A-Za-z0-9′.\-]+|[\u4e00-\u9fff]+", r)
    return [i for i, n in enumerate(names) if toks and all(t in n for t in toks)]

PAGE0_CELL_RE = re.compile(r'_r\d+c0$')   # 第 0 頁是表格：每列第一格（<table>_r<i>c0）= 名詞

def term_key(name):
    """名詞比對鍵：去空白、去掉結尾的一組括號（「symlink（根檔）」→「symlink」、「resolve／apply（兩段式）」→「resolve／apply」）。"""
    return re.sub(r'[（(][^（）()]*[）)]$', '', norm(name))

def page0_term_names(pages0):
    """第 0 頁的名詞集合（term_key 後）：名詞表 terms 的 name ＋ 表格每列第一格。"""
    names = set()
    for d in pages0:
        for t in d['terms']:
            if t['name']: names.add(term_key(t['name']))
        for n in d['nodes']:
            if n['cls'] == 'CELL' and PAGE0_CELL_RE.search(n['id']) and n['text']: names.add(term_key(n['text']))
    names.discard('')
    return names

def graph(d):
    """隱形邊（hidden）在 HIDDEN_EDGE=True 時視為不存在（不進 outs／ins）。"""
    nodes = d['nodes']; byid = {n['id']: n for n in nodes}
    edges = [e for e in d['edges'] if e['source'] in byid and e['target'] in byid and not (HIDDEN_EDGE and e.get('hidden'))]
    outs = defaultdict(list); ins = defaultdict(list)
    for e in edges: outs[e['source']].append(e); ins[e['target']].append(e)
    return nodes, byid, edges, outs, ins

def strip_branch_prefix(t): return WRITE_PREFIX_RE.sub('', t.replace('⏎', ' ').strip())

def is_write_step(n):
    if n['kind'] != 'step': return False
    t = strip_branch_prefix(n['text'])
    if any(t.startswith(f) for f in WRITE_LINE_FORCE): return True
    m = WRITE_VERB_RE.search(t)
    if not m: return False
    if m.group(1):                                       # 以寫入動詞開頭：看動詞後緊接的詞
        rest = t[m.end():].lstrip(' ：:')
        if any(rest.startswith(x) for x in WRITE_LINE_EXEMPT): return False
    if any(x in t for x in WRITE_LINE_EXEMPT_ANY): return False
    return True

def resolve_3way_walk(d, start_id, ctx):
    """從 start 沿出邊走，回傳 (A, B)：A = 含「回 0／結束碼 0／非 0」的 decision，B = 另一個含「文法／6-30」的 decision／step（A≠B），找不到就 None。
    只有白 step／decision 算一步；SUB（藍）、file、note、entry 不計；出口「續「X」頁」→ 接 X 頁「來自」入口（跨頁）；到終點就停。"""
    A = []; B = []
    seen = set(); frontier = [(d, start_id, 0)]
    while frontier:
        page, cid, depth = frontier.pop(0)
        ppid = page['page']['id']; key = (ppid, cid)
        if key in seen: continue
        seen.add(key)
        nodes, byid, edges, outs, ins = ctx['graphs'][ppid]
        n = byid.get(cid)
        if n is None: continue
        is_start = (ppid == d['page']['id'] and cid == start_id)
        if not is_start:
            if n['kind'] == 'decision' and RESOLVE_EXIT_RE.search(n['text']): A.append(key)
            if n['kind'] in ('decision', 'step') and RESOLVE_GRAMMAR_RE.search(n['text']): B.append(key)
            if n['kind'] in ('end_ok', 'end_orange', 'end_red'): continue
        counted = (not is_start) and n['kind'] == 'step' and n['cls'] != 'SUB'
        nd = depth + (1 if counted else 0)
        if nd > RESOLVE_3WAY_DEPTH: continue
        if n['kind'] == 'entry' and '續「' in n['text'] and '來自' not in n['text']:
            if RESOLVE_3WAY_CROSS_PAGE:
                for x in re.findall(r'續「([^」]{1,60})」頁', n['text']):
                    for ti in xref_targets(x, ctx['page_names']):
                        tp = ctx['pages_by_name'].get(ctx['page_names'][ti])
                        if not tp: continue
                        for en in tp['nodes']:
                            if en['kind'] == 'entry' and '來自「' in en['text']: frontier.append((tp, en['id'], nd))
            continue
        for e in outs[cid]: frontier.append((page, e['target'], nd))
    for a in A:
        for b in B:
            if a != b: return a, b
    return (A[0] if A else None), (B[0] if B and (not A or B[0] != A[0]) else None)

def lint_page(d, page_names, out, ctx=None):
    pid = d['page']['id']; name = d['page']['name']
    nodes, byid, edges, outs, ins = graph(d)
    add = lambda rule, level, cid, msg: out.append(dict(page=pid, page_name=name, rule=rule, level=level, id=cid, msg=msg))
    is_flow = bool(FLOW_PAGE_RE.search(name))
    ctx = ctx or dict(graphs={pid: (nodes, byid, edges, outs, ins)}, pages_by_name={name: d}, page_names=page_names, page0_terms=set(), seq={pid: 0})

    # ---- dangling ----
    if not is_flow:
        add('dangling', 'info', '-', '非流程頁，略過懸空檢查')
    else:
        for n in nodes:
            k = n['kind']; i, o = len(ins[n['id']]), len(outs[n['id']])
            if k in ('step', 'decision'):
                if i == 0 and o == 0: add('dangling', 'warn', n['id'], f'{k} 無進邊也無出邊：「{n["text"][:40]}」')
                elif i == 0: add('dangling', 'warn', n['id'], f'{k} 無進邊：「{n["text"][:40]}」')
                elif o == 0: add('dangling', 'warn', n['id'], f'{k} 無出邊：「{n["text"][:40]}」')
            elif k in ('end_orange', 'end_red'):
                if i == 0: add('dangling', 'warn', n['id'], f'{k} 無進邊：「{n["text"][:40]}」')
            elif k == 'end_ok':
                if i == 0 and o == 0: add('dangling', 'warn', n['id'], f'綠橢圓無進邊也無出邊：「{n["text"][:40]}」')
            elif k == 'entry':                                   # 白虛線橢圓：入口（來自「X」頁，要有出邊）／出口（續「X」頁，要有進邊；v2.15-3）
                if '續「' in n['text'] and '來自' not in n['text']:
                    if i == 0: add('dangling', 'warn', n['id'], f'出口無進邊：「{n["text"][:40]}」')
                elif o == 0: add('dangling', 'warn', n['id'], f'入口無出邊：「{n["text"][:40]}」')
            elif n['cls'] == 'IMG':
                if i == 0 and o == 0: add('dangling', 'info', n['id'], f'image 框沒有任何線：「{n["text"][:40]}」')

    # ---- decision ----
    for n in nodes:
        if n['kind'] != 'decision': continue
        o = outs[n['id']]
        if len(o) != 2: add('decision', 'warn', n['id'], f'菱形出邊數 {len(o)}（{", ".join(e["id"] for e in o) or "無"}）：「{n["text"][:40]}」')
        labels = [e['label'].replace('⏎', ' ') for e in o]
        for e, lab in zip(o, labels):
            if not YESNO_RE.match(lab): add('decision', 'info', e['id'], f'菱形 {n["id"]} 出邊標籤不以是／否開頭：「{lab or "(無標籤)"}」')
        if len(labels) == 2 and labels[0] and labels[0] == labels[1]:
            add('decision', 'warn', n['id'], f'兩條出邊標籤相同「{labels[0]}」（{o[0]["id"]}, {o[1]["id"]}）')

    # ---- endcolor ----
    for n in nodes:
        k = n['kind']; t = n['text']
        if k not in ('end_ok', 'end_orange', 'end_red'): continue
        if re.search(r'→\s*0\b|(^|[^\d])0：', t) and k != 'end_ok':
            add('endcolor', 'warn', n['id'], f'文字像成功（0）但是 {k}：「{t[:40]}」')
        if k == 'end_ok' and re.search(r'→\s*[123]\b|^[123]：', t):
            add('endcolor', 'warn', n['id'], f'綠終點文字含 1／2／3：「{t[:40]}」')
        if k == 'end_red' and any(w in t for w in NEEDS_HUMAN):
            add('endcolor', 'info', n['id'], f'紅終點文字含需人動作字眼（候選改橙）：「{t[:40]}」')

    # ---- xref ----
    for x in d['xrefs']:
        r = xref_ok(x['ref'], page_names)
        if r is None: add('xref', 'warn', x['id'], f'引用「{x["ref"]}」頁在 {len(page_names)} 頁名單找不到')
        elif r == 'fuzzy': add('xref', 'info', x['id'], f'引用「{x["ref"]}」頁只靠拆字比對到')

    # ---- base ----
    for n in nodes + [dict(id=e['id'], text=e['label']) for e in d['edges']]:
        t = n['text']
        if not re.search(r'\bbase\b', t): continue
        t2 = t
        for a in BASE_ALLOW: t2 = t2.replace(a, '')
        if re.search(r'\bbase\b', t2):
            m = re.search(r'.{0,20}\bbase\b.{0,20}', t2)
            add('base', 'warn', n['id'], f'出現 base 當實例：「…{m.group(0)}…」')

    # ---- color ----
    if not d['legend_fills']:
        add('color', 'info', '-', '此頁沒有圖例，略過顏色檢查')
    else:
        missing = [c for c in d['fills'] if c not in d['legend_fills'] and c not in COLOR_WHITELIST]
        for c in missing:
            ex = [n['id'] for n in nodes if n['fill'] == c and not n['legend']][:4]
            add('color', 'warn', ','.join(ex), f'fillColor {c} 不在圖例（{sum(1 for n in nodes if n["fill"] == c and not n["legend"])} 格，如 {ex}）')

    # ---- termcov ----
    tnames = ' '.join(t['name'] for t in d['terms']); ttexts = ' '.join(t['text'] for t in d['terms'])
    seen = {}
    for n in nodes:
        if n['kind'] in ('term',) or n['legend'] or n['cls'] in ('TITLE', 'TERM_H'): continue
        for label, rx in KEYWORDS:
            for m in re.finditer(rx, n['text']):
                hit = m.group(0)
                if hit in seen: continue
                if hit in tnames: seen[hit] = 'ok'
                elif hit in ttexts: seen[hit] = ('info', n['id'], label)
                else: seen[hit] = ('warn', n['id'], label)
    textonly = [hit for hit, v in seen.items() if v != 'ok' and v[0] == 'info']
    for hit, v in seen.items():
        if v == 'ok' or v[0] == 'info': continue
        lvl, cid, label = v
        add('termcov', 'warn', cid, f'「{hit}」（{label}）名詞表沒有對應條（name 與說明文都沒有）')
    if textonly:
        add('termcov', 'info', '-', f'{len(textonly)} 個關鍵字只在名詞說明文出現、沒有獨立條（略）：{"、".join(textonly[:12])}{"…" if len(textonly) > 12 else ""}')

    # ---- onething ----
    for n in nodes:
        if n['kind'] not in ('step', 'end_ok', 'end_orange', 'end_red'): continue
        cnt = {tok: n['text'].count(tok) for tok in ONETHING_TOKENS}
        total = sum(cnt.values())
        if total >= ONETHING_MIN:
            add('onething', 'info', n['id'], f'[{n["kind"]}] 分隔詞 {total}（' + ' '.join(f'{k}{v}' for k, v in cnt.items() if v) + f'）：「{n["text"]}」')

    # ======================= v2 新規則 =======================
    on = lambda r: ENABLED.get(r, True)
    starts = [n for n in nodes if n['kind'] == 'end_ok' and not ins[n['id']] and outs[n['id']]]
    file_nodes = {n['id'] for n in nodes if n['kind'] == 'file'}
    END_KINDS = ('end_ok', 'end_orange', 'end_red')

    # ---- event-name ----
    if on('event-name'):
        for n in nodes + [dict(id=e['id'], text=e['label']) for e in d['edges']]:
            m = EVENT_NAME_RE.search(n['text'])
            if m: add('event-name', 'warn', n['id'], f'舊事件名「{m.group(0)}」：事件名須用 spec 註冊表：launcher_start/exit、engine_start/exit（「{n["text"][:40]}」）')

    # ---- resolve-3way ----
    if on('resolve-3way') and is_flow:
        for n in nodes:
            if n['kind'] != 'step' or not RESOLVE_STEP_RE.search(n['text']): continue
            a, b = resolve_3way_walk(d, n['id'], ctx)
            if a and b: continue
            miss = []
            if not a: miss.append('缺「回 0／結束碼 0／非 0」判斷')
            if not b: miss.append('缺「文法／6-30」格' + ('（與結束碼判斷合在同一格）' if a else ''))
            add('resolve-3way', 'warn', n['id'], f'resolve 結果須三叉：非 0 原碼傳出／文法不合 6-30／合法 ── {"；".join(miss)}（{RESOLVE_3WAY_DEPTH} 步內{"、含跨頁" if RESOLVE_3WAY_CROSS_PAGE else ""}）：「{n["text"][:40]}」')

    # ---- precheck-recover ----
    if on('precheck-recover') and is_flow:
        first = bool(PRECHECK_FIRST_RE.search(name)) or not re.search(r'[（）]', name)
        cont = any(n['kind'] == 'entry' and '來自「' in n['text'] for n in nodes)
        if PRECHECK_SKIP_RE and PRECHECK_SKIP_RE.search(name): first = False
        if first and starts and not cont:
            if 'prune' in name:
                if not any('只列出' in n['text'] for n in nodes): add('precheck-recover', 'warn', '-', 'prune 第一頁須有「只列出」（活躍進度檔只列出不刪）')
            elif PRECHECK_SYNC_RE.search(name):
                if not any('6-33' in n['text'] for n in nodes if not n['legend'] and n['kind'] != 'term'):
                    add('precheck-recover', 'warn', '-', 'sync／update 第一頁須有節點文字含「6-33」（偵測到未完成交易）')
            elif PRECHECK_VERB_RE.search(name):
                if not any(n['kind'] == 'decision' and PRECHECK_DECISION_RE.search(n['text']) for n in nodes):
                    add('precheck-recover', 'warn', '-', '可寫動詞第一頁須有 decision 文字含「未完成」「既有進度檔」「恢復」（前置檢查／恢復）')

    # ---- end-color-text ----
    if on('end-color-text'):
        for n in nodes:
            k = n['kind']; t = n['text']
            if k not in END_KINDS: continue
            want = None
            if END_OK_RE.search(t): want = 'end_ok'
            elif END_RED_RE.search(t): want = 'end_red'
            elif END_ORANGE_RE.search(t): want = 'end_orange'
            if want and want != k:
                add('end-color-text', 'warn', n['id'], f'終點文字應為 {want} 但是 {k}：「{t[:40]}」')

    # ---- xref-forward ----
    if on('xref-forward') and ctx['seq'].get(pid) is not None:
        cur = ctx['seq'][pid]
        for x in d['xrefs']:
            if x['kind'] == '續': continue
            src = byid.get(x['id'])
            if src is not None and src['kind'] == 'entry' and '續「' in src['text'] and '來自' not in src['text']: continue
            tis = xref_targets(x['ref'], page_names)
            seqs = [ctx['seq'][ctx['page_ids'][i]] for i in tis if ctx['page_ids'][i] in ctx['seq']]
            # 同一動詞系列內往後「見」（例如 add（1）見 add（2）、bootstrap 見 install）允許：只擋跨系列前引。
            # 系列 = 頁名去掉序號前綴與括號後的第一個詞（bootstrap.sh／install／add／sync／upgrade／dev／undev／remove／uninstall／prune／update／離線包）。
            def _series(n):
                n = re.sub(r'^\d+ ', '', n); n = re.sub(r'^流程 v2：', '', n)
                m = re.match(r'([A-Za-z_.]+|離線包|升引擎)', n); return m.group(1).lower() if m else n
            same = any(_series(page_names[i]) == _series(page_names[ctx['page_ids'].index(pid)]) for i in tis) if tis else False
            if same and _series(page_names[ctx['page_ids'].index(pid)]) in ('bootstrap.sh', 'install', 'add', 'sync', 'upgrade', 'dev', 'undev', 'remove', 'uninstall', 'prune', 'update', '離線包'):
                continue
            if _series(page_names[ctx['page_ids'].index(pid)]) == 'bootstrap.sh' and tis and all(_series(page_names[i]) in ('install', 'add') for i in tis):
                continue   # bootstrap 呼叫 install／add 是它的定義，允許往後見
            if seqs and min(seqs) > cur:
                add('xref-forward', 'warn', x['id'], f'前引：頁 {cur} 只能引用序號更小的頁，卻{x["kind"] if x["kind"] != "其他" else "引用"}「{x["ref"]}」頁（序號 {min(seqs)}）')

    # ---- hidden-edge ----
    if on('hidden-edge'):
        for e in d['edges']:
            if e.get('hidden'):
                add('hidden-edge', 'warn', e['id'], f'隱形邊（visible=0）：{e["source"]} → {e["target"]}；lint 視為不存在，請改成可見線或刪掉')

    # ---- write-line / write-fail-edge ----
    if WRITE_PAGE_RE.search(name):
        for n in nodes:
            if not is_write_step(n): continue
            o = outs[n['id']]
            if on('write-line') and file_nodes and not any(e['target'] in file_nodes for e in o):
                add('write-line', 'warn', n['id'], f'寫入格缺到檔案框的線：「{n["text"][:40]}」')
            if on('write-fail-edge'):   # 只看可見出邊（graph() 已排除隱形邊）
                has_fail = any(byid[e['target']]['kind'] in ('end_red', 'end_orange') or WRITE_FAIL_HUB_RE.search(byid[e['target']]['text']) or '失敗' in e['label'] for e in o)
                if not has_fail:
                    add('write-fail-edge', 'warn', n['id'], f'寫入格缺可見失敗出邊（到紅／橙終點、失敗匯流格或標籤含「失敗」）：「{n["text"][:40]}」')

    # ---- term-count / term-dup-page0 ----
    if on('term-count') and len(d['terms']) > TERM_MAX and pid not in REVIEW_PAGE_IDS:
        add('term-count', 'warn', '-', f'名詞表 {len(d["terms"])} 條 > {TERM_MAX}')
    if on('term-dup-page0') and pid not in PAGE0_IDS:
        for t in d['terms']:
            if term_key(t['name']) in ctx['page0_terms']:
                add('term-dup-page0', 'warn', t['name'], f'名詞「{t["name"]}」第 0 頁已有（同名或只差結尾括號），不必重列')

    # ---- page-height / edge-font ----
    if on('page-height') and nodes and pid not in REVIEW_PAGE_IDS:
        bottom = max(n['y'] + n['h'] for n in nodes)
        if bottom > PAGE_MAX_H:
            low = max(nodes, key=lambda n: n['y'] + n['h'])
            add('page-height', 'warn', low['id'], f'頁高 {bottom} > {PAGE_MAX_H}（最低格 {low["id"]}「{low["text"][:20]}」）')
    if on('edge-font'):
        bad = [e for e in d['edges'] if e.get('fontSize') not in (None, EDGE_FONT)]
        for e in bad: add('edge-font', 'warn', e['id'], f'線標籤 fontSize={e["fontSize"]} ≠ {EDGE_FONT}：「{e["label"][:30]}」')

    # ---- merge-fanout ----
    if on('merge-fanout') and is_flow:
        for n in nodes:
            if n['kind'] != 'step': continue
            o = outs[n['id']]
            if len(o) >= MERGE_FANOUT_MIN and all(byid[e['target']]['kind'] in END_KINDS for e in o):
                add('merge-fanout', 'warn', n['id'], f'終點扇出：分支來源不可辨（{len(o)} 條出邊全到終點）：「{n["text"][:40]}」')

def lint_terms(pages, out):
    by = defaultdict(lambda: defaultdict(list))     # name -> text -> [pid]
    for d in pages:
        for t in d['terms']:
            if t['name']: by[t['name']][t['text']].append(d['page']['id'])
    for name, variants in sorted(by.items()):
        if len(variants) < 2: continue
        vs = sorted(variants.items(), key=lambda kv: -len(kv[1]))
        lines = [f'名詞「{name}」有 {len(vs)} 個版本：']
        for i, (text, pids) in enumerate(vs):
            lines.append(f'  v{i + 1}（{len(pids)} 頁：{" ".join(pids)}）長度 {len(text)}')
        a, b = vs[0][0], vs[1][0]
        sm = difflib.SequenceMatcher(None, a, b)
        diffs = []
        for op, i1, i2, j1, j2 in sm.get_opcodes():
            if op == 'equal': continue
            diffs.append(f'{op}: v1「{a[max(0, i1 - 8):i2 + 8]}」 ↔ v2「{b[max(0, j1 - 8):j2 + 8]}」')
            if len(diffs) >= 3: break
        lines.append('  v1↔v2 差異：' + ' ｜ '.join(diffs) if diffs else '  （僅空白差異）')
        out.append(dict(page='跨頁', page_name='共用名詞不一致', rule='term-diff', level='warn', id=name, msg='\n'.join(lines)))

def render(items, pages):
    by = defaultdict(list)
    for it in items: by[it['page']].append(it)
    L = ['# lint.md', '', f'頁數 {len(pages)}；條目 {len(items)}（warn {sum(1 for i in items if i["level"] == "warn")}、info {sum(1 for i in items if i["level"] == "info")}）', '']
    rc = Counter((i['rule'], i['level']) for i in items)
    L.append('| 規則 | warn | info |'); L.append('|---|---|---|')
    order = ['dangling', 'decision', 'endcolor', 'xref', 'term-diff', 'base', 'color', 'termcov', 'onething'] + list(ENABLED)
    for r in order + sorted({i['rule'] for i in items} - set(order)):
        L.append(f'| {r} | {rc[(r, "warn")]} | {rc[(r, "info")]} |')
    L.append('')
    for d in pages:
        pid = d['page']['id']
        its = by.get(pid, [])
        L.append(f'## {pid} {d["page"]["name"]}')
        L.append(f'nodes {len(d["nodes"])}／edges {len(d["edges"])}／terms {len(d["terms"])}；warn {sum(1 for i in its if i["level"] == "warn")}、info {sum(1 for i in its if i["level"] == "info")}')
        for it in its:
            L.append(f'- [{it["rule"]}][{it["level"]}] {it["id"]}: {it["msg"]}')
        L.append('')
    if by.get('跨頁'):
        L.append('## 跨頁：共用名詞不一致（term-diff）')
        for it in by['跨頁']:
            L.append(f'- [term-diff][warn] {it["id"]}:')
            for ln in it['msg'].split('\n')[1:]: L.append('    ' + ln)
        L.append('')
    return '\n'.join(L)

def main():
    if len(sys.argv) < 2: print(__doc__); sys.exit(2)
    outdir = sys.argv[1]
    pages, names = load_pages(outdir)
    page_names = [p['name'] for p in names]; page_ids = [p['id'] for p in names]
    by_id = {d['page']['id']: d for d in pages}
    ctx = dict(
        graphs={d['page']['id']: graph(d) for d in pages},
        pages_by_name={d['page']['name']: d for d in pages},
        page_names=page_names, page_ids=page_ids,
        seq={p['id']: page_seq(p['name'], i) for i, p in enumerate(names)},
        page0_terms=page0_term_names([by_id[pid0] for pid0 in PAGE0_IDS if pid0 in by_id]),
    )
    items = []
    for d in pages: lint_page(d, page_names, items, ctx)
    lint_terms(pages, items)
    md = render(items, pages)
    open(os.path.join(outdir, 'lint.md'), 'w', encoding='utf-8').write(md)
    json.dump(items, open(os.path.join(outdir, 'lint.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(md.split('\n\n')[1]); print('\n'.join(md.split('\n')[4:16]))
    print(f'→ {outdir}/lint.md, lint.json')

if __name__ == '__main__':
    main()
