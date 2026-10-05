"""drawio 匯出 PNG 的後處理：透明底改白底、等比縮圖、看基本資訊、清舊圖、比對時間。

drawio MCP 的 export_diagram 匯出的 PNG 是透明底（#138）。這支只用標準函式庫，
用 zlib＋struct 自己解碼／編碼 PNG，不需要主機另外安裝影像套件。

用法：
  python3 script/diagram/png.py info <png>
  python3 script/diagram/png.py flatten <in.png> <out.png>
  python3 script/diagram/png.py resize <in.png> <out.png> [--max-width 1600]
  python3 script/diagram/png.py clear <file>…
  python3 script/diagram/png.py finish --ref <drawio 檔> [--max-width 1600] <名.raw.png>…
  python3 script/diagram/png.py fresh --ref <檔> <file>…

- info：寬高、位元深度、色彩型態。
- flatten：RGBA 以 alpha 合成到白底，輸出 RGB PNG；輸入已是 RGB 就原樣重新編碼。
- resize：寬度大於 --max-width 時等比縮到該寬度（最近鄰取樣），否則尺寸不變；
  色彩型態沿用輸入。
- clear：刪掉存在的檔。輸出 removed（這次刪掉的檔）；刪完還有任何一個存在就 ok false。
- finish：每個檔名都要以 .raw.png 結尾（否則用法錯）。對每個做
  <名>.raw.png → flatten → <名>.flat.png → resize → <名>.png；某頁讀不到、壞掉或型態不支援就記進
  errors（{file, error}），其他頁照做。全部做完再做時間比對：成功的每頁，raw 與產出的
  png 的修改時間都不准早於 --ref。輸出 pngs（產出的 png）、stale、errors、ref、ref_mtime；
  有 errors 或 stale 就 ok false。
- fresh：只做時間比對。每個檔的修改時間都不准早於 --ref；檔不存在也算 stale（mtime null）。
  輸出 ref、ref_mtime、stale（[{file, mtime}]）；有 stale 就 ok false。
  --ref 讀不到時 finish／fresh 都回結束碼 1。
- 支援的型態只有 drawio 實際會輸出的：8-bit RGBA（color type 6）與 8-bit RGB（color type 2），
  非交錯。其他型態回結束碼 2 並說明。
- 輸出只保留 IHDR／IDAT／IEND，其他附屬 chunk 丟掉。

輸出一行 JSON 到 stdout：{"ok", "cmd", ...}；結束碼 0 過、1 有問題（檔案讀不到、不是 PNG、內容壞掉、
clear 沒刪乾淨、finish／fresh 有 stale 或 errors）、
2 用法錯（參數錯、不支援的 PNG 型態）。
"""
import argparse
import json
import os
import struct
import sys
import zlib

SIGNATURE = b"\x89PNG\r\n\x1a\n"
CHANNELS = {2: 3, 6: 4}  # color type → 每像素位元組數（8-bit）
COLOR_NAMES = {0: "gray", 2: "RGB", 3: "palette", 4: "gray+alpha", 6: "RGBA"}
DEFAULT_MAX_WIDTH = 1600


class PngError(Exception):
    """檔案不是 PNG 或內容壞掉（結束碼 1）。"""


class Unsupported(Exception):
    """是 PNG，但型態不在支援範圍（結束碼 2）。"""


class UsageError(Exception):
    """參數錯（結束碼 2）。"""


def _chunks(data: bytes):
    if not data.startswith(SIGNATURE):
        raise PngError("不是 PNG（檔頭簽章不符）")
    pos = len(SIGNATURE)
    while pos < len(data):
        if pos + 8 > len(data):
            raise PngError("chunk 長度欄位不完整")
        length, ctype = struct.unpack(">I4s", data[pos:pos + 8])
        body = data[pos + 8:pos + 8 + length]
        crc_raw = data[pos + 8 + length:pos + 12 + length]
        if len(body) != length or len(crc_raw) != 4:
            raise PngError(f"chunk {ctype!r} 被截斷")
        if zlib.crc32(ctype + body) != struct.unpack(">I", crc_raw)[0]:
            raise PngError(f"chunk {ctype!r} CRC 不符")
        yield ctype, body
        pos += 12 + length
        if ctype == b"IEND":
            return
    raise PngError("缺 IEND")


def read_header(data: bytes) -> dict:
    """只讀 IHDR，回傳 {width, height, bit_depth, color_type, interlace}。"""
    for ctype, body in _chunks(data):
        if ctype != b"IHDR":
            raise PngError("第一個 chunk 不是 IHDR")
        if len(body) != 13:
            raise PngError("IHDR 長度不對")
        w, h, depth, ctype_, comp, filt, inter = struct.unpack(">IIBBBBB", body)
        return {"width": w, "height": h, "bit_depth": depth, "color_type": ctype_,
                "compression": comp, "filter": filt, "interlace": inter}
    raise PngError("缺 IHDR")


def check_supported(hdr: dict) -> None:
    color = COLOR_NAMES.get(hdr["color_type"], f"未知({hdr['color_type']})")
    if hdr["color_type"] not in CHANNELS or hdr["bit_depth"] != 8:
        raise Unsupported(f"只支援 8-bit RGBA／RGB，這張是 {hdr['bit_depth']}-bit {color}")
    if hdr["interlace"] != 0:
        raise Unsupported("只支援非交錯 PNG，這張是 Adam7 交錯")
    if hdr["compression"] != 0 or hdr["filter"] != 0:
        raise Unsupported("壓縮或過濾方法不是標準的 0")


def _paeth(a: int, b: int, c: int) -> int:
    p = a + b - c
    pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
    if pa <= pb and pa <= pc:
        return a
    return b if pb <= pc else c


def decode(data: bytes):
    """回傳 (hdr, rows)；rows 是每列一個 bytearray（不含過濾位元組）。"""
    hdr = read_header(data)
    check_supported(hdr)
    idat = b"".join(body for ctype, body in _chunks(data) if ctype == b"IDAT")
    try:
        raw = zlib.decompress(idat)
    except zlib.error as e:
        raise PngError(f"IDAT 解壓失敗：{e}") from None
    bpp = CHANNELS[hdr["color_type"]]
    stride = hdr["width"] * bpp
    if len(raw) < hdr["height"] * (stride + 1):
        raise PngError("影像資料比宣告的寬高短")
    rows = []
    prev = bytearray(stride)
    pos = 0
    for _ in range(hdr["height"]):
        ftype = raw[pos]
        line = bytearray(raw[pos + 1:pos + 1 + stride])
        pos += stride + 1
        if ftype == 0:
            pass
        elif ftype == 1:
            for i in range(bpp, stride):
                line[i] = (line[i] + line[i - bpp]) & 0xFF
        elif ftype == 2:
            for i in range(stride):
                line[i] = (line[i] + prev[i]) & 0xFF
        elif ftype == 3:
            for i in range(stride):
                left = line[i - bpp] if i >= bpp else 0
                line[i] = (line[i] + ((left + prev[i]) >> 1)) & 0xFF
        elif ftype == 4:
            for i in range(stride):
                if i >= bpp:
                    left, upleft = line[i - bpp], prev[i - bpp]
                else:
                    left = upleft = 0
                line[i] = (line[i] + _paeth(left, prev[i], upleft)) & 0xFF
        else:
            raise PngError(f"不認得的過濾型態 {ftype}")
        rows.append(line)
        prev = line
    return hdr, rows


def _chunk(ctype: bytes, body: bytes) -> bytes:
    return struct.pack(">I", len(body)) + ctype + body + struct.pack(">I", zlib.crc32(ctype + body))


def encode(width: int, height: int, color_type: int, rows) -> bytes:
    """8-bit、非交錯、每列過濾型態 0。"""
    ihdr = struct.pack(">IIBBBBB", width, height, 8, color_type, 0, 0, 0)
    raw = b"".join(b"\x00" + bytes(r) for r in rows)
    return (SIGNATURE + _chunk(b"IHDR", ihdr)
            + _chunk(b"IDAT", zlib.compress(raw, 9)) + _chunk(b"IEND", b""))


def flatten_rows(color_type: int, rows):
    """RGBA → 白底 RGB；RGB 原樣。回傳 (color_type, rows)。"""
    if color_type == 2:
        return 2, rows
    out = []
    for r in rows:
        line = bytearray(len(r) // 4 * 3)
        j = 0
        for i in range(0, len(r), 4):
            a = r[i + 3]
            inv = 255 - a
            line[j] = (r[i] * a + 255 * inv + 127) // 255
            line[j + 1] = (r[i + 1] * a + 255 * inv + 127) // 255
            line[j + 2] = (r[i + 2] * a + 255 * inv + 127) // 255
            j += 3
        out.append(line)
    return 2, out


def resize_rows(width: int, height: int, bpp: int, rows, max_width: int):
    """寬度超過 max_width 就等比縮（最近鄰）。回傳 (w, h, rows)。"""
    if width <= max_width:
        return width, height, rows
    nw = max_width
    nh = max(1, round(height * nw / width))
    cols = [min(width - 1, x * width // nw) * bpp for x in range(nw)]
    out = []
    for y in range(nh):
        src = rows[min(height - 1, y * height // nh)]
        line = bytearray(nw * bpp)
        for x, sx in enumerate(cols):
            line[x * bpp:(x + 1) * bpp] = src[sx:sx + bpp]
        out.append(line)
    return nw, nh, out


def _read(path: str) -> bytes:
    try:
        with open(path, "rb") as f:
            return f.read()
    except OSError as e:
        raise PngError(f"讀不到 {path}：{e.strerror}") from None


def _write(path: str, data: bytes) -> None:
    try:
        with open(path, "wb") as f:
            f.write(data)
    except OSError as e:
        raise PngError(f"寫不進 {path}：{e.strerror}") from None


def _describe(hdr: dict) -> dict:
    return {"width": hdr["width"], "height": hdr["height"], "bit_depth": hdr["bit_depth"],
            "color_type": hdr["color_type"],
            "color": COLOR_NAMES.get(hdr["color_type"], f"未知({hdr['color_type']})"),
            "interlace": hdr["interlace"]}


def cmd_info(args) -> dict:
    hdr = read_header(_read(args.png))
    out = {"file": args.png, **_describe(hdr)}
    try:
        check_supported(hdr)
        out["supported"] = True
    except Unsupported as e:
        out["supported"] = False
        out["reason"] = str(e)
    return out


def flatten_file(src: str, dst: str) -> dict:
    hdr, rows = decode(_read(src))
    ctype, rows = flatten_rows(hdr["color_type"], rows)
    _write(dst, encode(hdr["width"], hdr["height"], ctype, rows))
    return {"input": src, "output": dst,
            "width": hdr["width"], "height": hdr["height"],
            "from": COLOR_NAMES[hdr["color_type"]], "to": COLOR_NAMES[ctype]}


def resize_file(src: str, dst: str, max_width: int) -> dict:
    hdr, rows = decode(_read(src))
    bpp = CHANNELS[hdr["color_type"]]
    nw, nh, rows = resize_rows(hdr["width"], hdr["height"], bpp, rows, max_width)
    _write(dst, encode(nw, nh, hdr["color_type"], rows))
    return {"input": src, "output": dst,
            "from": [hdr["width"], hdr["height"]], "to": [nw, nh],
            "resized": nw != hdr["width"], "color": COLOR_NAMES[hdr["color_type"]]}


def _check_max_width(max_width: int) -> None:
    if max_width < 1:
        raise UsageError("--max-width 要是正整數")


def cmd_flatten(args) -> dict:
    return flatten_file(args.input, args.output)


def cmd_resize(args) -> dict:
    _check_max_width(args.max_width)
    return resize_file(args.input, args.output, args.max_width)


def cmd_clear(args) -> dict:
    removed = []
    for path in args.files:
        if os.path.lexists(path):
            try:
                os.remove(path)
                removed.append(path)
            except OSError:
                pass
    left = [p for p in args.files if os.path.lexists(p)]
    out = {"ok": not left, "removed": removed}
    if left:
        out["left"] = left
    return out


def _ref_mtime(ref: str) -> float:
    try:
        return os.path.getmtime(ref)
    except OSError as e:
        raise PngError(f"讀不到基準檔 {ref}：{e.strerror}") from None


def stale_files(ref_mtime: float, files) -> list:
    """修改時間早於 ref_mtime 或不存在的檔：[{file, mtime}]，不存在的 mtime 是 None。"""
    bad = []
    for path in files:
        try:
            t = os.path.getmtime(path)
        except OSError:
            bad.append({"file": path, "mtime": None})
            continue
        if t < ref_mtime:
            bad.append({"file": path, "mtime": t})
    return bad


def cmd_fresh(args) -> dict:
    t = _ref_mtime(args.ref)
    stale = stale_files(t, args.files)
    return {"ok": not stale, "ref": args.ref, "ref_mtime": t, "stale": stale}


RAW_SUFFIX = ".raw.png"


def cmd_finish(args) -> dict:
    _check_max_width(args.max_width)
    bad = [p for p in args.raws if not p.endswith(RAW_SUFFIX)]
    if bad:
        raise UsageError(f"檔名要以 {RAW_SUFFIX} 結尾：{'、'.join(bad)}")
    t = _ref_mtime(args.ref)
    pngs, errors, done = [], [], []
    for raw in args.raws:
        stem = raw[:-len(RAW_SUFFIX)]
        flat, out = f"{stem}.flat.png", f"{stem}.png"
        try:
            flatten_file(raw, flat)
            resize_file(flat, out, args.max_width)
        except (PngError, Unsupported) as e:
            errors.append({"file": raw, "error": str(e)})
            continue
        pngs.append(out)
        done += [raw, out]
    stale = stale_files(t, done)
    return {"ok": not errors and not stale, "pngs": pngs, "stale": stale, "errors": errors,
            "ref": args.ref, "ref_mtime": t}


class _Parser(argparse.ArgumentParser):
    def error(self, message):
        raise UsageError(message)


def build_parser() -> argparse.ArgumentParser:
    p = _Parser(description="drawio 匯出 PNG 的白底與縮圖")
    sub = p.add_subparsers(dest="cmd", required=True, parser_class=_Parser)
    i = sub.add_parser("info")
    i.add_argument("png")
    f = sub.add_parser("flatten")
    f.add_argument("input")
    f.add_argument("output")
    r = sub.add_parser("resize")
    r.add_argument("input")
    r.add_argument("output")
    r.add_argument("--max-width", type=int, default=DEFAULT_MAX_WIDTH)
    c = sub.add_parser("clear")
    c.add_argument("files", nargs="+")
    fi = sub.add_parser("finish")
    fi.add_argument("--ref", required=True)
    fi.add_argument("--max-width", type=int, default=DEFAULT_MAX_WIDTH)
    fi.add_argument("raws", nargs="+")
    fr = sub.add_parser("fresh")
    fr.add_argument("--ref", required=True)
    fr.add_argument("files", nargs="+")
    return p


COMMANDS = {"info": cmd_info, "flatten": cmd_flatten, "resize": cmd_resize,
            "clear": cmd_clear, "finish": cmd_finish, "fresh": cmd_fresh}


def main(argv=None) -> int:
    cmd = None
    try:
        args = build_parser().parse_args(argv)
        cmd = args.cmd
        result = {"ok": True, "cmd": cmd, **COMMANDS[cmd](args)}
        code = 0 if result["ok"] else 1
    except (UsageError, Unsupported) as e:
        result, code = {"ok": False, "cmd": cmd, "error": str(e)}, 2
    except PngError as e:
        result, code = {"ok": False, "cmd": cmd, "error": str(e)}, 1
    print(json.dumps(result, ensure_ascii=False))
    return code


if __name__ == "__main__":
    sys.exit(main())
