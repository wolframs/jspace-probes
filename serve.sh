#!/bin/sh
# Serve the lab: dashboard at http://localhost:8321/dashboard/
#
# Sends Cache-Control: no-store on everything. `python -m http.server` sends no
# cache headers at all, so Chrome applies a heuristic cache and keeps serving a
# stale app.js / findings.json after an edit — which cost two rounds of "the fix
# isn't showing up". Development only; the deployed site sets its own caching.
cd "$(dirname "$0")"
exec python3 - <<'PY'
import http.server, socketserver

class NoCache(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, must-revalidate")
        super().end_headers()

socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", 8321), NoCache) as srv:
    print("serving http://localhost:8321/dashboard/ (no-store)")
    srv.serve_forever()
PY
