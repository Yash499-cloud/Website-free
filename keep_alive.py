#!/usr/bin/env python3
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

class KeepAliveHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.handle_request()
    
    def do_HEAD(self):
        self.handle_request()
    
    def handle_request(self):
        if self.path in ('/', '/health'):
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            # Only write body for GET requests
            if self.command == 'GET':
                response = json.dumps({"status": "alive", "agent": "ready"})
                self.wfile.write(response.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        # Clean logging format
        print(f"{self.address_string()} - {format % args}")

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 8080), KeepAliveHandler)
    print('Keep-alive server running on 0.0.0.0:8080')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nShutting down server...')
        server.shutdown()
