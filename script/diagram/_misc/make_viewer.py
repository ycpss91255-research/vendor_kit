"""把 drawio 包成可用瀏覽器直接看的 HTML（draw.io 官方 viewer，只讀、可切頁、可縮放）。"""
import html, json, sys
src, out, title = sys.argv[1], sys.argv[2], sys.argv[3]
xml = open(src).read()
cfg = {"highlight": "#0000ff", "nav": True, "resize": True, "lightbox": False, "toolbar": "pages zoom layers", "xml": xml}
page = f"""<!doctype html><html><head><meta charset="utf-8"><title>{html.escape(title)}</title>
<meta http-equiv="Cache-Control" content="no-store"><style>body{{margin:0;background:#fff}}</style></head><body>
<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{html.escape(json.dumps(cfg, ensure_ascii=False), quote=True)}"></div>
<script src="https://viewer.diagrams.net/js/viewer-static.min.js"></script></body></html>"""
open(out, "w").write(page); print(out, len(page))
