#!/usr/bin/env python3
"""Dev server for the slideshow.

Serves the static site like `python3 -m http.server`, plus accepts
PUT/POST to /media.json so the editor's Save button can write the file.

Usage:  python3 server.py [port]     (default 8100)
"""
import json
import os
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.abspath(__file__))


class Handler(SimpleHTTPRequestHandler):
    def do_PUT(self):
        self._save()

    def do_POST(self):
        self._save()

    def _save(self):
        # Only media.json is writable — everything else stays read-only.
        if self.path.split("?")[0] != "/media.json":
            self.send_error(404, "Only /media.json is writable")
            return
        length = int(self.headers.get("Content-Length", 0))
        if not 0 < length <= 10_000_000:
            self.send_error(413, "Payload missing or too large")
            return
        raw = self.rfile.read(length)
        try:
            data = json.loads(raw)
        except Exception as e:
            self.send_error(400, f"Invalid JSON: {e}")
            return
        # Atomic write: temp file then rename, so a crash never corrupts media.json.
        tmp = os.path.join(ROOT, "media.json.tmp")
        with open(tmp, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")
        os.replace(tmp, os.path.join(ROOT, "media.json"))
        body = b'{"ok":true}'
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def end_headers(self):
        # media.json must never be stale in the player/editor.
        if self.path.split("?")[0] == "/media.json":
            self.send_header("Cache-Control", "no-store")
        super().end_headers()


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8100
    os.chdir(ROOT)
    print(f"Serving {ROOT} on 0.0.0.0:{port} (PUT /media.json enabled)")
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()
