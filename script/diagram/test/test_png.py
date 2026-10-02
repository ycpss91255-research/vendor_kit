"""png.py：PNG 白底、縮圖、資訊、清舊圖、批次收尾、時間比對。測試用的 PNG 都由程式產生。"""
import json
import os
import pathlib
import struct
import subprocess
import sys
import tempfile
import unittest
import zlib
from contextlib import redirect_stdout
from io import StringIO

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import png  # noqa: E402


def chunk(ctype, body):
    return struct.pack(">I", len(body)) + ctype + body + struct.pack(">I", zlib.crc32(ctype + body))


def paeth(a, b, c):
    p = a + b - c
    pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
    if pa <= pb and pa <= pc:
        return a
    return b if pb <= pc else c


def filter_line(ftype, line, prev, bpp):
    out = bytearray(len(line))
    for i in range(len(line)):
        left = line[i - bpp] if i >= bpp else 0
        up = prev[i]
        upleft = prev[i - bpp] if i >= bpp else 0
        pred = {0: 0, 1: left, 2: up, 3: (left + up) >> 1, 4: paeth(left, up, upleft)}[ftype]
        out[i] = (line[i] - pred) & 0xFF
    return bytes([ftype]) + bytes(out)


def make_png(width, height, color_type, pixels, filters=(0,), depth=8, interlace=0, extra=b""):
    """pixels[y][x] 是 tuple；filters 依列輪流用。"""
    bpp = {2: 3, 6: 4}.get(color_type, 1)
    raw = b""
    prev = bytes(width * bpp)
    for y in range(height):
        line = bytes(v for px in pixels[y] for v in px)
        raw += filter_line(filters[y % len(filters)], line, prev, bpp)
        prev = line
    ihdr = struct.pack(">IIBBBBB", width, height, depth, color_type, 0, 0, interlace)
    return (png.SIGNATURE + chunk(b"IHDR", ihdr) + extra
            + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b""))


def run(*argv):
    buf = StringIO()
    with redirect_stdout(buf):
        code = png.main(list(argv))
    lines = buf.getvalue().splitlines()
    assert len(lines) == 1, lines
    return code, json.loads(lines[0])


def gradient(width, height, alpha=True):
    return [[(x * 37 % 256, y * 53 % 256, (x + y) * 11 % 256) + ((x * y * 7 % 256,) if alpha else ())
             for x in range(width)] for y in range(height)]


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = pathlib.Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, name, data):
        p = self.dir / name
        p.write_bytes(data)
        return str(p)


class Decode(Base):
    def test_all_filter_types_roundtrip(self):
        for ct, alpha in ((6, True), (2, False)):
            px = gradient(7, 10, alpha)
            hdr, rows = png.decode(make_png(7, 10, ct, px, filters=(0, 1, 2, 3, 4)))
            self.assertEqual((hdr["width"], hdr["height"], hdr["color_type"]), (7, 10, ct))
            want = [bytes(v for p in r for v in p) for r in px]
            self.assertEqual([bytes(r) for r in rows], want)

    def test_encode_then_decode(self):
        px = gradient(5, 4)
        rows = [bytearray(v for p in r for v in p) for r in px]
        hdr, back = png.decode(png.encode(5, 4, 6, rows))
        self.assertEqual(back, rows)

    def test_ancillary_chunks_skipped(self):
        data = make_png(2, 2, 6, gradient(2, 2), extra=chunk(b"tEXt", b"k\x00v"))
        hdr, rows = png.decode(data)
        self.assertEqual(len(rows), 2)


class Flatten(Base):
    def test_rgba_to_white_rgb(self):
        px = [[(0, 0, 0, 0), (0, 0, 0, 255), (255, 0, 0, 128), (10, 20, 30, 255)]]
        src = self.write("a.png", make_png(4, 1, 6, px))
        out = str(self.dir / "b.png")
        code, res = run("flatten", src, out)
        self.assertEqual(code, 0, res)
        self.assertEqual((res["from"], res["to"]), ("RGBA", "RGB"))
        hdr, rows = png.decode(pathlib.Path(out).read_bytes())
        self.assertEqual(hdr["color_type"], 2)
        self.assertEqual(list(rows[0]), [255, 255, 255, 0, 0, 0, 255, 127, 127, 10, 20, 30])

    def test_rgb_kept(self):
        px = gradient(3, 3, alpha=False)
        src = self.write("a.png", make_png(3, 3, 2, px))
        out = str(self.dir / "b.png")
        code, res = run("flatten", src, out)
        self.assertEqual(code, 0)
        _, rows = png.decode(pathlib.Path(out).read_bytes())
        self.assertEqual([bytes(r) for r in rows], [bytes(v for p in r for v in p) for r in px])


class Resize(Base):
    def test_shrinks_to_max_width_keeping_ratio(self):
        src = self.write("a.png", make_png(40, 20, 6, gradient(40, 20)))
        out = str(self.dir / "b.png")
        code, res = run("resize", src, out, "--max-width", "10")
        self.assertEqual(code, 0, res)
        self.assertEqual((res["from"], res["to"], res["resized"]), ([40, 20], [10, 5], True))
        hdr, rows = png.decode(pathlib.Path(out).read_bytes())
        self.assertEqual((hdr["width"], hdr["height"], hdr["color_type"]), (10, 5, 6))
        self.assertEqual(len(rows[0]), 40)

    def test_nearest_sampling(self):
        px = [[(x, 0, 0) for x in range(4)]]
        _, _, rows = png.resize_rows(4, 1, 3, [bytearray(v for p in px[0] for v in p)], 2)
        self.assertEqual(list(rows[0]), [0, 0, 0, 2, 0, 0])

    def test_small_image_unchanged(self):
        src = self.write("a.png", make_png(8, 4, 2, gradient(8, 4, alpha=False)))
        out = str(self.dir / "b.png")
        code, res = run("resize", src, out)
        self.assertEqual(code, 0)
        self.assertEqual((res["to"], res["resized"]), ([8, 4], False))

    def test_default_max_width(self):
        self.assertEqual(png.build_parser().parse_args(["resize", "a", "b"]).max_width, 1600)

    def test_bad_max_width(self):
        src = self.write("a.png", make_png(2, 2, 6, gradient(2, 2)))
        code, res = run("resize", src, str(self.dir / "b.png"), "--max-width", "0")
        self.assertEqual(code, 2)
        self.assertFalse(res["ok"])


class Info(Base):
    def test_rgba(self):
        src = self.write("a.png", make_png(3, 2, 6, gradient(3, 2)))
        code, res = run("info", src)
        self.assertEqual(code, 0)
        self.assertEqual((res["width"], res["height"], res["color"], res["supported"]), (3, 2, "RGBA", True))

    def test_unsupported_reported_not_failed(self):
        src = self.write("g.png", make_png(2, 2, 0, [[(1,), (2,)], [(3,), (4,)]]))
        code, res = run("info", src)
        self.assertEqual(code, 0)
        self.assertEqual((res["color"], res["supported"]), ("gray", False))


def small_rgba(width=4, height=2):
    """用 png.py 自己的 encode 產生小 RGBA PNG。"""
    rows = [bytearray(v for px in r for v in px) for r in gradient(width, height)]
    return png.encode(width, height, 6, rows)


class TimeBase(Base):
    REF_T = 1_700_000_000

    def setUp(self):
        super().setUp()
        self.ref = self.write("x.drawio", b"<mxfile/>")
        os.utime(self.ref, (self.REF_T, self.REF_T))

    def age(self, path, delta):
        """把 path 的修改時間設成 ref 加 delta 秒。"""
        os.utime(path, (self.REF_T + delta, self.REF_T + delta))


class Clear(Base):
    def test_removes_existing_and_ignores_missing(self):
        a = self.write("a.raw.png", b"x")
        b = self.write("a.png", b"y")
        missing = str(self.dir / "nope.png")
        code, res = run("clear", a, missing, b)
        self.assertEqual(code, 0, res)
        self.assertEqual((res["ok"], res["cmd"], res["removed"]), (True, "clear", [a, b]))
        self.assertFalse(os.path.exists(a) or os.path.exists(b))

    def test_all_missing_ok(self):
        code, res = run("clear", str(self.dir / "nope.png"))
        self.assertEqual((code, res["ok"], res["removed"]), (0, True, []))

    def test_cannot_remove_not_ok(self):
        d = self.dir / "dir.png"
        d.mkdir()  # 目錄刪不掉（os.remove 不刪目錄）
        code, res = run("clear", str(d))
        self.assertEqual(code, 1)
        self.assertFalse(res["ok"])
        self.assertEqual(res["removed"], [])

    def test_needs_a_file(self):
        code, res = run("clear")
        self.assertEqual(code, 2)


class Fresh(TimeBase):
    def test_all_newer_ok(self):
        a = self.write("a.png", b"x")
        self.age(a, 5)
        same = self.write("b.png", b"x")
        self.age(same, 0)
        code, res = run("fresh", "--ref", self.ref, a, same)
        self.assertEqual(code, 0, res)
        self.assertEqual((res["ok"], res["cmd"], res["ref"], res["ref_mtime"], res["stale"]),
                         (True, "fresh", self.ref, self.REF_T, []))

    def test_older_and_missing_are_stale(self):
        old = self.write("old.png", b"x")
        self.age(old, -5)
        new = self.write("new.png", b"x")
        self.age(new, 5)
        missing = str(self.dir / "nope.png")
        code, res = run("fresh", "--ref", self.ref, old, new, missing)
        self.assertEqual(code, 1)
        self.assertFalse(res["ok"])
        self.assertEqual(res["stale"], [{"file": old, "mtime": self.REF_T - 5},
                                        {"file": missing, "mtime": None}])

    def test_missing_ref_exit_1(self):
        code, res = run("fresh", "--ref", str(self.dir / "nope.drawio"), self.ref)
        self.assertEqual(code, 1)
        self.assertFalse(res["ok"])

    def test_needs_ref(self):
        code, res = run("fresh", self.ref)
        self.assertEqual(code, 2)


class Finish(TimeBase):
    def test_flatten_resize_each_page(self):
        a = self.write("p1.raw.png", small_rgba(40, 20))
        b = self.write("p2.raw.png", small_rgba(4, 2))
        code, res = run("finish", "--ref", self.ref, "--max-width", "10", a, b)
        self.assertEqual(code, 0, res)
        pa, pb = str(self.dir / "p1.png"), str(self.dir / "p2.png")
        self.assertEqual((res["ok"], res["cmd"], res["pngs"], res["stale"], res["errors"]),
                         (True, "finish", [pa, pb], [], []))
        self.assertEqual((res["ref"], res["ref_mtime"]), (self.ref, self.REF_T))
        self.assertTrue((self.dir / "p1.flat.png").exists())
        hdr, _ = png.decode(pathlib.Path(pa).read_bytes())
        self.assertEqual((hdr["width"], hdr["height"], hdr["color_type"]), (10, 5, 2))
        hdr, _ = png.decode(pathlib.Path(pb).read_bytes())
        self.assertEqual((hdr["width"], hdr["height"], hdr["color_type"]), (4, 2, 2))

    def test_default_max_width(self):
        args = png.build_parser().parse_args(["finish", "--ref", "x.drawio", "a.raw.png"])
        self.assertEqual(args.max_width, 1600)

    def test_bad_page_recorded_others_done(self):
        good = self.write("good.raw.png", small_rgba())
        broken = self.write("broken.raw.png", b"hello")
        missing = str(self.dir / "missing.raw.png")
        code, res = run("finish", "--ref", self.ref, broken, missing, good)
        self.assertEqual(code, 1)
        self.assertFalse(res["ok"])
        self.assertEqual(res["pngs"], [str(self.dir / "good.png")])
        self.assertEqual([e["file"] for e in res["errors"]], [broken, missing])
        self.assertTrue(all(e["error"] for e in res["errors"]))
        self.assertEqual(res["stale"], [])

    def test_raw_older_than_ref_is_stale(self):
        raw = self.write("p.raw.png", small_rgba())
        self.age(raw, -5)
        code, res = run("finish", "--ref", self.ref, raw)
        self.assertEqual(code, 1)
        self.assertFalse(res["ok"])
        self.assertEqual(res["stale"], [{"file": raw, "mtime": self.REF_T - 5}])
        self.assertEqual(res["pngs"], [str(self.dir / "p.png")])

    def test_ref_newer_than_outputs_is_stale(self):
        raw = self.write("p.raw.png", small_rgba())
        future = 4_000_000_000
        os.utime(self.ref, (future, future))
        code, res = run("finish", "--ref", self.ref, raw)
        self.assertEqual(code, 1)
        self.assertEqual([s["file"] for s in res["stale"]], [raw, str(self.dir / "p.png")])

    def test_name_must_end_with_raw_png_exit_2(self):
        a = self.write("a.png", small_rgba())
        code, res = run("finish", "--ref", self.ref, a)
        self.assertEqual(code, 2)
        self.assertFalse(res["ok"])
        self.assertIn(".raw.png", res["error"])
        self.assertFalse((self.dir / "a.flat.png").exists())

    def test_cli_exit_2_on_bad_name(self):
        script = pathlib.Path(png.__file__)
        p = subprocess.run([sys.executable, str(script), "finish", "--ref", self.ref, "a.png"],
                           capture_output=True, text=True)
        self.assertEqual(p.returncode, 2)
        self.assertFalse(json.loads(p.stdout)["ok"])

    def test_bad_max_width_exit_2(self):
        raw = self.write("p.raw.png", small_rgba())
        code, res = run("finish", "--ref", self.ref, "--max-width", "0", raw)
        self.assertEqual(code, 2)

    def test_missing_ref_exit_1(self):
        raw = self.write("p.raw.png", small_rgba())
        code, res = run("finish", "--ref", str(self.dir / "nope.drawio"), raw)
        self.assertEqual(code, 1)
        self.assertFalse(res["ok"])


class Errors(Base):
    def test_gray_unsupported_exit_2(self):
        src = self.write("g.png", make_png(2, 2, 0, [[(1,), (2,)], [(3,), (4,)]]))
        code, res = run("flatten", src, str(self.dir / "o.png"))
        self.assertEqual(code, 2)
        self.assertIn("8-bit RGBA", res["error"])

    def test_16bit_unsupported_exit_2(self):
        ihdr = struct.pack(">IIBBBBB", 1, 1, 16, 6, 0, 0, 0)
        data = png.SIGNATURE + chunk(b"IHDR", ihdr) + chunk(b"IDAT", zlib.compress(bytes(9))) + chunk(b"IEND", b"")
        code, res = run("resize", self.write("d.png", data), str(self.dir / "o.png"))
        self.assertEqual(code, 2)

    def test_interlaced_exit_2(self):
        src = self.write("i.png", make_png(2, 2, 6, gradient(2, 2), interlace=1))
        code, res = run("flatten", src, str(self.dir / "o.png"))
        self.assertEqual(code, 2)
        self.assertIn("交錯", res["error"])

    def test_not_png_exit_1(self):
        code, res = run("info", self.write("x.png", b"hello"))
        self.assertEqual(code, 1)
        self.assertFalse(res["ok"])

    def test_bad_crc_exit_1(self):
        data = bytearray(make_png(2, 2, 6, gradient(2, 2)))
        data[20] ^= 0xFF  # 改 IHDR 內容，CRC 就不符
        code, res = run("info", self.write("c.png", bytes(data)))
        self.assertEqual(code, 1)

    def test_missing_file_exit_1(self):
        code, res = run("info", str(self.dir / "nope.png"))
        self.assertEqual(code, 1)

    def test_usage_exit_2(self):
        code, res = run("flatten", "only-one")
        self.assertEqual(code, 2)
        code, res = run("bogus")
        self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()
