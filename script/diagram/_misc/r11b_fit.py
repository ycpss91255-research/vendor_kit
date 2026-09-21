"""測文字在某寬／樣式下的高度：python3 r11b_fit.py <style: D|W|G|O|R|S> <w> <text>..."""
import sys
exec(open("disc_v1_b.py").read().split("# ---------- 泳道流程佈局 ----------")[0])
ST = dict(D=D12, W=W12, G=G12, O=O12, R=R12, S=SUB, F=F12, N=NOTE, RU=RULE)
st = ST[sys.argv[1]]; w = int(sys.argv[2])
for t in sys.argv[3:]:
    print(fit_h(fl(t), fit_w(fl(t), w, st), 40, 0, st), fit_w(fl(t), w, st), t)
