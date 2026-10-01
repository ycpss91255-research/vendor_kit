"""png.py：PNG 白底、縮圖、資訊。測試用的 PNG 都由程式產生。"""
import json
import pathlib
import struct
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
