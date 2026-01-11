"""
Launcher - Main Entry Point for Standalone Executable
Starts backend server and opens frontend in browser
"""

import os
import sys
import time
import webbrowser
import threading
from pathlib import Path

# Add backend to path
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    base_path = Path(sys._MEIPASS)
else:
    # Running as script
    base_path = Path(__file__).parent

sys.path.insert(0, str(base_path / 'backend'))

def start_backend():
    """Start the Flask backend server"""
    print("🚀 Starting backend server...")
    os.chdir(str(base_path / 'backend'))
    
    # Import and run Flask app
    from backend.app import app
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

def start_frontend():
    """Start frontend server"""
    print("🌐 Starting frontend server...")
    os.chdir(str(base_path / 'frontend'))
    
    import http.server
    import socketserver
    
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", 8000), Handler) as httpd:
        print("✅ Frontend running on http://localhost:8000")
        httpd.serve_forever()

def open_browser():
    """Open browser after short delay"""
    time.sleep(3)  # Wait for servers to start
    print("🌐 Opening browser...")
    webbrowser.open('http://localhost:8000')

if __name__ == '__main__':
    print("=" * 60)
    print("🎯 AI Keyword Classifier")
    print("=" * 60)
    
    # Start backend in separate thread
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()
    
    # Start browser opener in separate thread
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    # Start frontend in main thread (blocks)
    try:
        start_frontend()
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
        sys.exit(0)
