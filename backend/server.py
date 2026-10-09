#!/usr/bin/env python3
"""Backend server for 다, 너의 단어.

Connects the backend to the frontend:
  - serves the static frontend/ app
  - exposes a real state API the frontend syncs to:
      GET  /api/health        -> {"ok": true}
      GET  /api/state         -> {"data": <saved blob or null>}
      PUT  /api/state  {data}  -> {"ok": true}   (persists to backend/state.json)

Stdlib only, no external dependencies. The frontend stays a static client; this
adds a durable server-side store for the user's 단어장/메모/설정 blob.

Run:  python3 backend/server.py            (defaults to 127.0.0.1:8934)
      PORT=9000 python3 backend/server.py
"""

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FRONTEND = ROOT / "frontend"
STATE_FILE = Path(__file__).resolve().parent / "state.json"
MAX_BODY = 20 * 1024 * 1024  # mirror the app's 20k-char / backup cap, generously

CONTENT_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".js": "text/javascript; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".svg": "image/svg+xml",
    ".txt": "text/plain; charset=utf-8",
    ".ico": "image/x-icon",
}


def _load_state():
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except Exception:
        return None


def _save_state(data):
    STATE_FILE.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")


class Handler(BaseHTTPRequestHandler):
    server_version = "daneoword/1.0"

    def _send(self, code, body=b"", ctype="application/json; charset=utf-8"):
        if isinstance(body, str):
            body = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def _json(self, code, obj):
        self._send(code, json.dumps(obj, ensure_ascii=False))

    # --- API ---
    def do_GET(self):
        if self.path == "/api/health":
            return self._json(200, {"ok": True})
        if self.path == "/api/state":
            return self._json(200, {"data": _load_state()})
        return self._serve_static()

    def do_HEAD(self):
        self._serve_static()

    def do_PUT(self):
        if self.path != "/api/state":
            return self._json(404, {"error": "not found"})
        length = int(self.headers.get("Content-Length", 0))
        if length <= 0 or length > MAX_BODY:
            return self._json(400, {"error": "bad length"})
        try:
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            data = payload.get("data")
        except Exception:
            return self._json(400, {"error": "bad json"})
        _save_state(data)
        return self._json(200, {"ok": True})

    # --- static frontend ---
    def _serve_static(self):
        rel = self.path.split("?", 1)[0].lstrip("/")
        if rel in ("", "/"):
            rel = "index.html"
        target = (FRONTEND / rel).resolve()
        # prevent path traversal outside frontend/
        if FRONTEND not in target.parents and target != FRONTEND:
            return self._json(403, {"error": "forbidden"})
        if not target.is_file():
            return self._json(404, {"error": "not found"})
        ctype = CONTENT_TYPES.get(target.suffix, "application/octet-stream")
        self._send(200, target.read_bytes(), ctype)

    def log_message(self, fmt, *args):
        pass  # quiet


def main():
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "8934"))
    httpd = ThreadingHTTPServer((host, port), Handler)
    print(f"다, 너의 단어 server: http://{host}:{port}/  (state -> {STATE_FILE})")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.shutdown()


if __name__ == "__main__":
    main()
