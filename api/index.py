import sys
import os
import json
import traceback
from http.server import BaseHTTPRequestHandler

# Add root and db directory to path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(ROOT_DIR, "db")
if DB_DIR not in sys.path:
    sys.path.insert(0, DB_DIR)
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

try:
    # pyrefly: ignore [missing-import]
    import api_router
except Exception as _import_err:
    api_router = None
    _import_err_str = traceback.format_exc()


class handler(BaseHTTPRequestHandler):
    def _send_err(self, status, err_msg, details=None):
        payload = {"error": err_msg}
        if details:
            payload["details"] = details
        content = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()
        self.wfile.write(content)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def do_GET(self):
        if not api_router:
            return self._send_err(500, "Backend router failed to initialize", _import_err_str)
        try:
            return api_router.handle_get(self)
        except Exception as e:
            return self._send_err(500, "Internal Server Error", str(e))

    def do_POST(self):
        if not api_router:
            return self._send_err(500, "Backend router failed to initialize", _import_err_str)
        try:
            return api_router.handle_post(self)
        except Exception as e:
            return self._send_err(500, "Internal Server Error", str(e))

    def do_PUT(self):
        if not api_router:
            return self._send_err(500, "Backend router failed to initialize", _import_err_str)
        try:
            return api_router.handle_put(self)
        except Exception as e:
            return self._send_err(500, "Internal Server Error", str(e))

    def do_DELETE(self):
        if not api_router:
            return self._send_err(500, "Backend router failed to initialize", _import_err_str)
        try:
            return api_router.handle_delete(self)
        except Exception as e:
            return self._send_err(500, "Internal Server Error", str(e))
