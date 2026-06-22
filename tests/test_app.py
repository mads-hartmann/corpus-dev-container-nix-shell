import json
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer

from app import Handler, response_for


class ResponseTests(unittest.TestCase):
    def test_healthz_payload(self):
        self.assertEqual(response_for("/healthz"), (200, {"ok": True}))

    def test_root_payload_names_environment(self):
        status, payload = response_for("/")

        self.assertEqual(status, 200)
        self.assertEqual(payload["environment"], "nix-shell")

    def test_running_server_serves_healthz(self):
        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)

        url = f"http://127.0.0.1:{server.server_address[1]}/healthz"
        with urllib.request.urlopen(url, timeout=2) as response:
            body = json.loads(response.read())

        self.assertEqual(response.status, 200)
        self.assertEqual(body, {"ok": True})

    def test_missing_route_returns_404(self):
        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)

        url = f"http://127.0.0.1:{server.server_address[1]}/missing"
        with self.assertRaises(urllib.error.HTTPError) as caught:
            urllib.request.urlopen(url, timeout=2)

        self.assertEqual(caught.exception.code, 404)
        caught.exception.close()


if __name__ == "__main__":
    unittest.main()
