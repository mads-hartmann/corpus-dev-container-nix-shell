import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


def response_for(path):
    if path == "/healthz":
        return 200, {"ok": True}
    if path == "/":
        return 200, {
            "service": "corpus-dev-container-nix-shell",
            "environment": "nix-shell",
        }
    return 404, {"error": "not found"}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        status, payload = response_for(self.path)
        body = json.dumps(payload, sort_keys=True).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        return


def main():
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", os.environ.get("CORPUS_SERVICE_PORT", "8000")))
    server = ThreadingHTTPServer((host, port), Handler)
    print(f"Serving on http://{host}:{port}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
