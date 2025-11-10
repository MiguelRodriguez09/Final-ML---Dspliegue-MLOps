#!/usr/bin/env python3
"""
Simple HTTP Server for MLOps Frontend
Serves the static frontend files with CORS enabled
"""

import os
import http.server
import socketserver
from http.server import SimpleHTTPRequestHandler

# Puerto configurable via variable de entorno
PORT = int(os.environ.get('PORT', 8080))

class CORSRequestHandler(SimpleHTTPRequestHandler):
    """
    Custom request handler with CORS headers
    """
    
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()
    
    def log_message(self, format, *args):
        """Custom log format with colors"""
        message = format % args
        print(f"[Frontend Server] {message}")

def run_server():
    """Start the HTTP server"""
    
    # Change to the directory containing this script
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Create the server
    with socketserver.TCPServer(("", PORT), CORSRequestHandler) as httpd:
        print("=" * 60)
        print("🎨 MLOps Frontend Server")
        print("=" * 60)
        print(f"✅ Server running at: http://localhost:{PORT}")
        print(f"📁 Serving directory: {os.getcwd()}")
        print(f"🔗 API endpoint: http://localhost:5000")
        print("=" * 60)
        print("Press Ctrl+C to stop the server")
        print("=" * 60)
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n🛑 Server stopped by user")
            print("Goodbye! 👋")

if __name__ == "__main__":
    run_server()
