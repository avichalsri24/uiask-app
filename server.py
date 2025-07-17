#!/usr/bin/env python3
import http.server
import socketserver
import os
import json
import urllib.request
import urllib.parse
from urllib.error import HTTPError

# Configuration
PORT = int(os.getenv('PORT', 8000))
HOST = os.getenv('HOST', '0.0.0.0')
UIPATH_TOKEN = os.getenv('UIPATH_TOKEN', '')

class CORSHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, accept, accept-language, x-uipath-internal-tenantid, referer')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        if self.path.startswith('/api/proxy'):
            self.handle_api_proxy()
        else:
            super().do_POST()

    def do_GET(self):
        if self.path.startswith('/api/proxy'):
            self.handle_api_proxy()
        else:
            super().do_GET()

    def handle_api_proxy(self):
        try:
            if not UIPATH_TOKEN:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'UIPATH_TOKEN not configured'}).encode())
                return
            
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length) if content_length > 0 else None
            
            parsed_path = urllib.parse.urlparse(self.path)
            query_params = urllib.parse.parse_qs(parsed_path.query)
            
            if 'url' not in query_params:
                self.send_error(400, "Missing 'url' parameter")
                return
                
            target_url = urllib.parse.unquote(query_params['url'][0])
            req = urllib.request.Request(target_url, data=post_data, method=self.command)
            
            # Copy headers
            for header_name in ['content-type', 'accept', 'accept-language', 'x-uipath-internal-tenantid', 'referer']:
                if header_name in self.headers:
                    req.add_header(header_name, self.headers[header_name])
            
            req.add_header('authorization', f'Bearer {UIPATH_TOKEN}')
            
            try:
                with urllib.request.urlopen(req) as response:
                    self.send_response(response.getcode())
                    for header, value in response.headers.items():
                        if header.lower() not in ['content-length', 'transfer-encoding']:
                            self.send_header(header, value)
                    self.end_headers()
                    self.wfile.write(response.read())
                    
            except HTTPError as e:
                self.send_response(e.code)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': f'HTTP {e.code}', 'message': str(e)}).encode())
                
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Internal Server Error', 'message': str(e)}).encode())

    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {format % args}")

def start_server():
    try:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        
        if not UIPATH_TOKEN:
            print("⚠️ Warning: UIPATH_TOKEN environment variable not set")
        
        with socketserver.TCPServer((HOST, PORT), CORSHTTPRequestHandler) as httpd:
            print(f"🚀 UiASK Server running at: http://{HOST}:{PORT}")
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    start_server() 