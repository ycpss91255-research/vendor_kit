"""文字是否超出方塊（估算）。用法: python3 check_overflow.py <file.drawio> [page_id ...]
估算：中文字 ≈ fontSize px、英數 ≈ 0.6×fontSize；每行寬 ≤ 折行寬−16；行數×(fontSize×1.3) ≤ 可用高−8。
<br>／\\n 算換行；超過寬度自動折行也算行數；swimlane 只算標題列（startSize）。
橢圓／菱形（v2.5 §15）：draw.io 以「外框寬 − spacingLeft − spacingRight」折行，不是以內接矩形折行，所以
  折行寬 = w − spacingLeft − spacingRight（style 沒有 spacing 就視為 0 → 用整個 w 折行）
  可用寬 = 有 spacing → 同折行寬；沒有 → 內接矩形 w×0.707（菱形 ×0.5）
  可用高 = h − spacingTop − spacingBottom；沒有 → h×0.707（菱形 ×0.5）
  每一行折出來的寬 > 可用寬 → 報「行太寬」（= 文字會超出橢圓輪廓）。
產生器請用 shape_spacing() 對橢圓／菱形自動加 spacing（橢圓 ×0.146、菱形 ×0.25），折行寬就等於內接矩形。"""
import re, html, sys, unicodedata
from drawio_common import load, vertices, args

def strip_tags(s):
    s = re.sub(r'<br\s*/?>', '\n', s, flags=re.I)
    s = re.sub(r'</?(b|i|u|font|span|div|p|strong|em)[^>]*>', '', s, flags=re.I)
    return html.unescape(s)          # 再解一次：&lt;repo&gt; → <repo>（畫面上真的顯示的字）

def cw(ch, fs):
    if ch == '\n': return 0
    return fs if unicodedata.east_asian_width(ch) in ('W', 'F') else 0.6 * fs

def tokens(line):
    """中文字每字一個 token；英數連續字一個 token（不能在中間斷）；空白也是 token。"""
    out = []; buf = ''
    for ch in line:
        if unicodedata.east_asian_width(ch) in ('W', 'F') or ch.isspace():
            if buf: out.append(buf); buf = ''
            out.append(ch)
        else: buf += ch
    if buf: out.append(buf)
    return out

def wrap(line, fs, maxw):
    """回傳 (行數, 最寬 token 寬度)。貪婪折行。"""
    return wrap_lines(line, fs, maxw)[:2]

def wrap_lines(line, fs, maxw):
    """回傳 (行數, 最寬 token 寬度, 最寬「折出來的行」寬度)。貪婪折行。"""
    n = 1; cur = 0; widest = 0; widest_line = 0
    for t in tokens(line):
        w = sum(cw(c, fs) for c in t); widest = max(widest, w)
        if cur + w > maxw and cur > 0 and not t.isspace():
            widest_line = max(widest_line, cur); n += 1; cur = w
        elif t.isspace() and cur + w > maxw: pass      # 折行點的空白被吃掉，不算寬
        else: cur += w
    widest_line = max(widest_line, cur)
    return n, widest, widest_line

# ---------- 橢圓／菱形 spacing（v2.5 §15）----------
ELLIPSE_K, RHOMBUS_K = 0.146, 0.25
def shape_kind(style):
    head = style.split(';')[0]
    if head == 'ellipse' or 'shape=ellipse' in style: return 'ellipse'
    if head == 'rhombus' or 'shape=rhombus' in style: return 'rhombus'
    return ''
def spacing_for(style, w, h):
    """橢圓／菱形該加的 spacing：回傳 (左右, 上下)；其他形狀回 None。"""
    k = shape_kind(style)
    if not k: return None
    f = ELLIPSE_K if k == 'ellipse' else RHOMBUS_K
    return round(w * f), round(h * f)
def shape_spacing(style, w, h):
    """產生器用：橢圓／菱形自動補 spacingLeft/Right = round(w×0.146)、spacingTop/Bottom = round(h×0.146)（菱形 ×0.25）；
    style 已含 spacingLeft 就不動；其他形狀原樣回傳。"""
    sp = spacing_for(style, w, h)
    if sp is None or 'spacingLeft=' in style: return style
    lr, tb = sp
    if not style.endswith(';'): style += ';'
    return style + f"spacingLeft={lr};spacingRight={lr};spacingTop={tb};spacingBottom={tb};"

def text_area(c):
    """回傳 (折行寬, 可用寬, 可用高, 形狀說明)；已含 −16／−8 邊距。"""
    st = c['style']; g = c['geo']
    w, h = float(g.get('width', 0)), float(g.get('height', 0))
    if c['shape'] == 'swimlane': h = float(st.get('startSize', 23))
    kind = shape_kind(c['attrs'].get('style', ''))
    if not kind: return w - 16, w - 16, h - 8, ''
    f = 0.707 if kind == 'ellipse' else 0.5
    has_sp = any(k in st for k in ('spacingLeft', 'spacingRight', 'spacingTop', 'spacingBottom'))
    sl, sr = float(st.get('spacingLeft', 0)), float(st.get('spacingRight', 0))
    stp, sb = float(st.get('spacingTop', 0)), float(st.get('spacingBottom', 0))
    wrapw = w - sl - sr
    availw = wrapw if (sl or sr) else w * f
    availh = (h - stp - sb) if (stp or sb) else h * f
    name = '橢圓' if kind == 'ellipse' else '菱形'
    return wrapw - 16, availw - 16, availh - 8, (name + ('(spacing)' if has_sp else '(無 spacing)'))

def check(cells, only=None):
    issues = []
    for c in vertices(cells):
        st = c['style']; g = c['geo']
        if not c['value'].strip(): continue
        w0, h0 = float(g.get('width', 0)), float(g.get('height', 0))
        fs = float(st.get('fontSize', 12))
        wrapw, maxw, maxh, shp = text_area(c)
        text = strip_tags(c['value'])
        lines = 0; over_w = []; over_l = []
        for ln in text.split('\n'):
            n, widest, wline = wrap_lines(ln, fs, wrapw); lines += n
            if widest > maxw: over_w.append((widest, ln))
            elif wline > maxw + 0.5: over_l.append((wline, ln))
        need_h = lines * fs * 1.3
        short = text.replace('\n', '⏎')[:40]
        for widest, ln in over_w:
            issues.append(f"{c['id']}: 單字太寬 {widest:.0f} > {maxw:.0f}（{shp}w={w0:.0f}）「{ln[:40]}」")
        for wline, ln in over_l:
            issues.append(f"{c['id']}: 行太寬 {wline:.0f} > 可用 {maxw:.0f}（{shp}w={w0:.0f}；折行寬 {wrapw:.0f}）「{ln[:40]}」")
        if need_h > maxh:
            issues.append(f"{c['id']}: 高度不夠 {lines} 行×{fs*1.3:.1f}={need_h:.0f} > {maxh:.0f}（{shp}h={h0:.0f}, w={w0:.0f}）「{short}」")
    return issues

if __name__ == '__main__':
    path, pages = args(); total = 0
    for pid, name, cells in load(path):
        if pages and pid not in pages: continue
        iss = check(cells); total += len(iss)
        print(f"== {pid} {name}"); [print("  ", i) for i in iss] or print("   無")
    print(f"共 {total} 筆"); sys.exit(1 if total else 0)
