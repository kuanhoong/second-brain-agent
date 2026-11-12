"""Live knowledge-graph viewer for the OKF bundle. Standard library only.

    python graph_server.py                 # http://localhost:8765, refreshes itself
    python graph_server.py --export viz.html   # one self-contained offline file

The page polls /api/graph, so nodes appear and change colour while the agent
works in `adk web`. Nothing is loaded from a CDN: it works with the Wi-Fi off.

It also receives highlights from the Chrome extension in extension/:
    POST /api/capture   {url, title, text}  ->  {id, state, source}
    GET  /api/capture?id=...                ->  the job, until state is done
"""
from __future__ import annotations

import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

try:  # adk web loads .env by itself; this server needs the key too, for captures
    from dotenv import load_dotenv

    load_dotenv(Path(__file__).resolve().parent / ".env")
except ImportError:
    pass

from second_brain import capture, okf

VIEWER = Path(__file__).resolve().parent / "viewer" / "index.html"


def note_payload(rid: str) -> dict | None:
    try:
        path = okf.resolve(rid)
    except ValueError:
        return None
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8")
    _, body = okf.parse_text(text)
    front = text.split("\n---", 1)[0].replace("---\n", "", 1) if text.startswith("---") else ""
    return {"id": rid, "frontmatter": front.strip(), "body": body}


class Handler(BaseHTTPRequestHandler):
    def _send(self, code: int, body: bytes, ctype: str) -> None:
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        url = urlparse(self.path)
        if url.path in ("/", "/index.html"):
            self._send(200, VIEWER.read_bytes(), "text/html; charset=utf-8")
        elif url.path == "/api/graph":
            self._send(200, json.dumps(okf.graph()).encode(), "application/json")
        elif url.path == "/api/capture":
            job = capture.JOBS.get(parse_qs(url.query).get("id", [""])[0])
            self._send(200 if job else 404, json.dumps(job or {}).encode(), "application/json")
        elif url.path == "/api/note":
            payload = note_payload(parse_qs(url.query).get("id", [""])[0])
            self._send(200 if payload else 404, json.dumps(payload or {}).encode(), "application/json")
        else:
            self._send(404, b"not found", "text/plain")

    def do_POST(self) -> None:  # noqa: N802
        if urlparse(self.path).path != "/api/capture":
            return self._send(404, b"not found", "text/plain")
        if not capture.allowed_origin(self.headers.get("Origin")):
            return self._send(403, b'{"error": "captures are accepted from the extension only"}', "application/json")
        try:
            length = int(self.headers.get("Content-Length") or 0)
            if length > 200_000:
                raise ValueError("Highlight too large.")
            data = json.loads(self.rfile.read(length) or b"{}")
            job = capture.start(str(data.get("url", "")), str(data.get("title", "")), str(data.get("text", "")))
        except (ValueError, json.JSONDecodeError) as exc:
            return self._send(400, json.dumps({"error": str(exc)}).encode(), "application/json")
        self._send(202, json.dumps(job).encode(), "application/json")

    def log_message(self, *args) -> None:  # keep the terminal quiet on stage
        pass


def export(out: Path) -> None:
    graph = okf.graph()
    notes = {n["id"]: note_payload(n["id"]) for n in graph["nodes"] if n["kind"] == "concept"}
    safe = lambda obj: json.dumps(obj).replace("</", "<\\/")  # noqa: E731
    html = VIEWER.read_text(encoding="utf-8")
    html = html.replace("/*__GRAPH__*/null", safe(graph)).replace("/*__NOTES__*/null", safe(notes))
    out.write_text(html, encoding="utf-8")
    print(f"Wrote {out} ({len(graph['nodes'])} nodes, {len(graph['edges'])} edges)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--export", metavar="FILE", help="write a self-contained HTML file and exit")
    args = parser.parse_args()
    if args.export:
        export(Path(args.export))
    else:
        print(f"Second brain graph: http://localhost:{args.port}   (vault: {okf.VAULT_DIR})")
        ThreadingHTTPServer(("127.0.0.1", args.port), Handler).serve_forever()
