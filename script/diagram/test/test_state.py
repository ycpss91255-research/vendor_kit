"""state.py：用假 HTTP server 與暫存檔測 get／put／check／diff，不依賴 drawio 服務。"""
import base64
import json
import pathlib
import subprocess
import sys
import tempfile
import threading
import unittest
import urllib.parse
import zlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

SCRIPT = pathlib.Path(__file__).resolve().parent.parent / "state.py"
sys.path.insert(0, str(SCRIPT.parent))
import state  # noqa: E402

SID = "mcp-test-0001"

TWO_PAGES = """<mxfile host="app.diagrams.net">
  <diagram id="pgA" name="頁A"><mxGraphModel><root>
    <mxCell id="0"/><mxCell id="1" parent="0"/>
    <mxCell id="2" value="甲" style="rounded=1;" vertex="1" parent="1"><mxGeometry x="40" y="40" width="120" height="60" as="geometry"/></mxCell>
    <mxCell id="3" value="乙" style="rounded=1;" vertex="1" parent="1"><mxGeometry x="240" y="40" width="120" height="60" as="geometry"/></mxCell>
  </root></mxGraphModel></diagram>
  <diagram id="pgB" name="頁B"><mxGraphModel><root>
    <mxCell id="0"/><mxCell id="1" parent="0"/>
  </root></mxGraphModel></diagram>
</mxfile>
"""

BLANK = ('<mxfile><diagram id="blank" name="Page-1"><mxGraphModel><root>'
         '<mxCell id="0"/><mxCell id="1" parent="0"/></root></mxGraphModel></diagram></mxfile>')


class FakeDrawio:
    """模擬 GET／POST /api/state。"""

    def __init__(self, xml=TWO_PAGES, version=5):
        self.xml, self.version, self.posts = xml, version, []
        owner = self

        class H(BaseHTTPRequestHandler):
            def log_message(self, *a):
                pass

            def _send(self, code, obj):
                body = json.dumps(obj).encode()
                self.send_response(code)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def do_GET(self):
                u = urllib.parse.urlsplit(self.path)
                q = urllib.parse.parse_qs(u.query)
                if u.path != "/api/state" or q.get("sessionId") != [SID]:
                    return self._send(404, {"error": "no session"})
                self._send(200, {"xml": owner.xml, "version": owner.version})

            def do_POST(self):
                data = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                owner.posts.append(data)
                if self.path != "/api/state" or data.get("sessionId") != SID:
                    return self._send(404, {"error": "no session"})
                owner.xml, owner.version = data["xml"], owner.version + 1
                self._send(200, {"success": True, "version": owner.version})

        self.srv = ThreadingHTTPServer(("127.0.0.1", 0), H)
        self.url = f"http://localhost:{self.srv.server_address[1]}/?mcp={SID}"
        threading.Thread(target=self.srv.serve_forever, daemon=True).start()

    def close(self):
        self.srv.shutdown()
        self.srv.server_close()


def run(*args):
    r = subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True)
    lines = r.stdout.strip().splitlines()
    assert len(lines) == 1, r.stdout + r.stderr
    return r.returncode, json.loads(lines[0])


def free_port():
    import socket
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = pathlib.Path(self.tmp.name)
        self.addCleanup(self.tmp.cleanup)

    def write(self, name, text):
        p = self.dir / name
        p.write_text(text, encoding="utf-8")
        return str(p)


class Session(Base):
    def test_parse_url(self):
        self.assertEqual(state.parse_page_url("http://localhost:6002/?mcp=abc"), ("http://127.0.0.1:6002", "abc"))

    def test_bad_url_is_usage(self):
        code, out = run("check", "--url", "http://localhost:6002/")
        self.assertEqual((code, out["reason"]), (2, "usage"))

    def test_session_file(self):
        srv = FakeDrawio()
        self.addCleanup(srv.close)
        f = self.write("s.txt", srv.url + "\n")
        code, out = run("check", "--session-file", f)
        self.assertEqual(code, 0, out)
        self.assertEqual(out["session"], SID)

    def test_session_file_missing(self):
        code, out = run("check", "--session-file", str(self.dir / "none.txt"))
        self.assertEqual(code, 2)

    def test_session_file_two_lines(self):
        f = self.write("s.txt", "http://localhost:1/?mcp=a\nhttp://localhost:2/?mcp=b\n")
        self.assertEqual(run("check", "--session-file", f)[0], 2)

    def test_default_file_is_workspace_reference(self):
        p = state.default_session_file()
        self.assertEqual(p.parts[-2:], ("reference", "drawio_session.txt"))

    def test_url_and_file_exclusive(self):
        self.assertEqual(run("check", "--url", "http://localhost:1/?mcp=a", "--session-file", "x")[0], 2)

    def test_no_subcommand(self):
        code, out = run()
        self.assertEqual((code, out["ok"]), (2, False))


class Check(Base):
    def test_live(self):
        srv = FakeDrawio()
        self.addCleanup(srv.close)
        code, out = run("check", "--url", srv.url)
        self.assertEqual(code, 0, out)
        self.assertEqual(out["version"], 5)
        self.assertEqual([p["id"] for p in out["pages"]], ["pgA", "pgB"])

    def test_blank_is_stale(self):
        srv = FakeDrawio(BLANK, 1)
        self.addCleanup(srv.close)
        code, out = run("check", "--url", srv.url)
        self.assertEqual((code, out["reason"]), (1, "blank"))

    def test_blank_with_later_version_is_live(self):
        srv = FakeDrawio(BLANK, 2)
        self.addCleanup(srv.close)
        self.assertEqual(run("check", "--url", srv.url)[0], 0)

    def test_unreachable(self):
        code, out = run("check", "--url", f"http://localhost:{free_port()}/?mcp={SID}", "--timeout", "2")
        self.assertEqual((code, out["reason"]), (1, "unreachable"))

    def test_unknown_session(self):
        srv = FakeDrawio()
        self.addCleanup(srv.close)
        code, out = run("check", "--url", srv.url.replace(SID, "other"))
        self.assertEqual((code, out["reason"]), (1, "http_error"))


class GetPut(Base):
    def test_get_writes_file(self):
        srv = FakeDrawio()
        self.addCleanup(srv.close)
        out_file = self.dir / "got.drawio"
        code, out = run("get", str(out_file), "--url", srv.url)
        self.assertEqual(code, 0, out)
        self.assertEqual(out_file.read_text(encoding="utf-8"), TWO_PAGES)

    def test_get_blank_does_not_write(self):
        srv = FakeDrawio(BLANK, 1)
        self.addCleanup(srv.close)
        out_file = self.dir / "got.drawio"
        self.assertEqual(run("get", str(out_file), "--url", srv.url)[0], 1)
        self.assertFalse(out_file.exists())

    def test_put_returns_version(self):
        srv = FakeDrawio(BLANK, 1)
        self.addCleanup(srv.close)
        f = self.write("in.drawio", TWO_PAGES)
        code, out = run("put", f, "--url", srv.url)
        self.assertEqual(code, 0, out)
        self.assertEqual(out["version"], 2)
        self.assertEqual(srv.posts, [{"sessionId": SID, "xml": TWO_PAGES}])

    def test_put_bad_xml_not_sent(self):
        srv = FakeDrawio()
        self.addCleanup(srv.close)
        f = self.write("in.drawio", "<mxfile><diagram")
        self.assertEqual(run("put", f, "--url", srv.url)[0], 1)
        self.assertEqual(srv.posts, [])

    def test_put_missing_file(self):
        self.assertEqual(run("put", str(self.dir / "none.drawio"), "--url", "http://localhost:1/?mcp=a")[0], 2)


def compress(model_xml):
    co = zlib.compressobj(9, zlib.DEFLATED, -15)
    raw = co.compress(urllib.parse.quote(model_xml).encode()) + co.flush()
    return base64.b64encode(raw).decode()


class Diff(Base):
    def diff(self, before, after):
        return run("diff", self.write("a.drawio", before), self.write("b.drawio", after))

    def test_same(self):
        code, out = self.diff(TWO_PAGES, TWO_PAGES)
        self.assertEqual(code, 0)
        self.assertFalse(out["changed"])

    def test_attribute_order_and_whitespace_ignored(self):
        after = TWO_PAGES.replace('value="甲" style="rounded=1;"', 'style="rounded=1;"  value="甲"')
        self.assertFalse(self.diff(TWO_PAGES, after)[1]["changed"])

    def test_cells(self):
        after = (TWO_PAGES.replace('value="乙"', 'value="乙2"')
                 .replace('<mxCell id="2" value="甲" style="rounded=1;" vertex="1" parent="1">'
                          '<mxGeometry x="40" y="40" width="120" height="60" as="geometry"/></mxCell>', "")
                 .replace('<mxCell id="1" parent="0"/>\n  </root>',
                          '<mxCell id="1" parent="0"/><mxCell id="9" vertex="1" parent="1"/>\n  </root>'))
        out = self.diff(TWO_PAGES, after)[1]
        self.assertEqual(out["cells"], {
            "pgA": {"added": [], "removed": ["2"], "changed": ["3"]},
            "pgB": {"added": ["9"], "removed": [], "changed": []},
        })
        self.assertEqual(out["id_changes"]["disappeared"], [])

    def test_rename(self):
        out = self.diff(TWO_PAGES, TWO_PAGES.replace('name="頁B"', 'name="頁乙"'))[1]
        self.assertEqual(out["pages"]["renamed"], [{"id": "pgB", "from": "頁B", "to": "頁乙"}])
        self.assertEqual(out["id_changes"]["appeared"], [])

    def test_id_changed(self):
        out = self.diff(TWO_PAGES, TWO_PAGES.replace('id="pgB"', 'id="pgC"'))[1]
        self.assertEqual(out["pages"]["added"], [{"id": "pgC", "name": "頁B"}])
        self.assertEqual(out["pages"]["removed"], [{"id": "pgB", "name": "頁B"}])
        self.assertEqual(out["id_changes"], {"disappeared": ["pgB"], "appeared": ["pgC"],
                                             "same_name": [{"name": "頁B", "from_id": "pgB", "to_id": "pgC"}]})
        self.assertNotIn("pgC", out["cells"])

    def test_compressed_page(self):
        model = ('<mxGraphModel><root><mxCell id="0"/><mxCell id="1" parent="0"/>'
                 '<mxCell id="5" vertex="1" parent="1"/></root></mxGraphModel>')
        before = f'<mxfile><diagram id="p" name="P">{compress(model)}</diagram></mxfile>'
        after = f'<mxfile><diagram id="p" name="P">{model}</diagram></mxfile>'
        self.assertFalse(self.diff(before, after)[1]["changed"])

    def test_duplicate_page_id(self):
        dup = TWO_PAGES.replace('id="pgB"', 'id="pgA"')
        code, out = self.diff(TWO_PAGES, dup)
        self.assertEqual((code, out["reason"]), (1, "bad_xml"))

    def test_bad_xml(self):
        self.assertEqual(self.diff(TWO_PAGES, "<mxfile>")[0], 1)

    def test_missing_file(self):
        self.assertEqual(run("diff", str(self.dir / "x"), str(self.dir / "y"))[0], 2)


if __name__ == "__main__":
    unittest.main()
