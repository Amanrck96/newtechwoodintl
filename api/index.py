import sys
import os
from http.server import BaseHTTPRequestHandler

# Add root and db directory to path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(ROOT_DIR, "db")
if DB_DIR not in sys.path:
    sys.path.insert(0, DB_DIR)
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import api_router

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

    def do_GET(self):
        return api_router.handle_get(self)

    def do_POST(self):
        return api_router.handle_post(self)

    def do_PUT(self):
        return api_router.handle_put(self)

    def do_DELETE(self):
        return api_router.handle_delete(self)
