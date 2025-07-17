#!/usr/bin/env python3
import http.server
import socketserver
import os
import json
import urllib.request
import urllib.parse
from urllib.error import HTTPError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration
PORT = int(os.environ.get('PORT', 8000))  # Use Render's PORT env variable
HOST = os.environ.get('HOST', '0.0.0.0')  # Bind to all interfaces for cloud deployment

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
            self.handle_proxy()
        else:
            super().do_POST()

    def do_GET(self):
        if self.path.startswith('/api/proxy'):
            self.handle_proxy()
        elif self.path == '/api/config':
            self.handle_config()
        else:
            super().do_GET()

    def handle_proxy(self):
        try:
            # Get the target URL from query params
            parsed_path = urllib.parse.urlparse(self.path)
            query_params = urllib.parse.parse_qs(parsed_path.query)
            
            if 'url' not in query_params:
                self.send_error(400, "Missing 'url' parameter")
                return
            
            target_url = urllib.parse.unquote(query_params['url'][0])
            print(f"🔄 Proxying to: {target_url}")
            
            # Get request body
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length) if content_length > 0 else None
            
            # Create the request
            req = urllib.request.Request(target_url, data=post_data, method=self.command)
            
            # Copy all headers from the original request
            for header_name, header_value in self.headers.items():
                if header_name.lower() not in ['host', 'content-length']:
                    req.add_header(header_name, header_value)
            
            # Make the request
            with urllib.request.urlopen(req) as response:
                print(f"✅ Response: {response.getcode()}")
                self.send_response(response.getcode())
                
                # Copy response headers
                for header, value in response.headers.items():
                    if header.lower() not in ['content-length', 'transfer-encoding']:
                        self.send_header(header, value)
                
                self.end_headers()
                self.wfile.write(response.read())
                
        except HTTPError as e:
            print(f"❌ HTTP Error: {e.code}")
            response_data = e.read().decode('utf-8') if hasattr(e, 'read') else str(e)
            print(f"❌ Response: {response_data[:500]}...")
            
            self.send_response(e.code)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(response_data.encode())
            
        except Exception as e:
            print(f"❌ Proxy error: {e}")
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())

    def handle_config(self):
        """Serve configuration including secure tokens from environment variables"""
        try:
            config = {
                'uipath_token': os.environ.get('UIPATH_TOKEN', ''),
                'tenant_id': os.environ.get('UIPATH_TENANT_ID', '93ca45a7-470c-4ff8-bad9-13675fad7267')
            }
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(config).encode())
            
        except Exception as e:
            print(f"❌ Config error: {e}")
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Failed to load configuration'}).encode())

def start_server():
    try:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        
        with socketserver.TCPServer((HOST, PORT), CORSHTTPRequestHandler) as httpd:
            print(f"🚀 UiASK Server running at: http://{HOST}:{PORT}")
            print("📂 Serving files from current directory")
            print("🌐 CORS enabled for all origins")
            print("🔄 Proxy enabled at /api/proxy")
            print("⏹️  Press Ctrl+C to stop")
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    start_server() 