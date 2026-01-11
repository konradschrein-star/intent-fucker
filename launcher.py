"""
Launcher - Fixed Version for PyInstaller Executable
Properly handles bundled resources and starts servers
"""

import os
import sys
import time
import webbrowser
import threading
from pathlib import Path

def get_base_path():
    """Get the correct base path for bundled or unbundled execution"""
    if getattr(sys, 'frozen', False):
        # Running as compiled executable - use temp extraction folder
        return Path(sys._MEIPASS)
    else:
        # Running as script - use current directory
        return Path(__file__).parent

def start_backend():
    """Start the Flask backend server"""
    try:
        base_path = get_base_path()
        backend_path = base_path / 'backend'
        
        print(f"🔍 Base path: {base_path}")
        print(f"🔍 Backend path: {backend_path}")
        print(f"🔍 Backend exists: {backend_path.exists()}")
        
        # Add backend to Python path
        sys.path.insert(0, str(backend_path))
        
        # Change to backend directory
        os.chdir(str(backend_path))
        
        print("🚀 Starting Flask backend...")
        
        # Import Flask app
        import app
        app.app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False, threaded=True)
        
    except Exception as e:
        print(f"❌ Backend error: {e}")
        import traceback
        traceback.print_exc()

def start_frontend():
    """Start frontend HTTP server"""
    try:
        base_path = get_base_path()
        frontend_path = base_path / 'frontend'
        
        print(f"🔍 Frontend path: {frontend_path}")
        print(f"🔍 Frontend exists: {frontend_path.exists()}")
        
        if not frontend_path.exists():
            print(f"❌ Frontend directory not found!")
            return
            
        # Change to frontend directory
        os.chdir(str(frontend_path))
        
        print("🌐 Starting frontend server on http://localhost:8000...")
        
        import http.server
        import socketserver
        
        class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
            def end_headers(self):
                # Add CORS headers
                self.send_header('Access-Control-Allow-Origin', '*')
                super().end_headers()
        
        with socketserver.TCPServer(("", 8000), MyHTTPRequestHandler) as httpd:
            print("✅ Frontend server running!")
            httpd.serve_forever()
            
    except Exception as e:
        print(f"❌ Frontend error: {e}")
        import traceback
        traceback.print_exc()

def open_browser():
    """Open browser after servers have started"""
    print("⏳ Waiting for servers to start...")
    time.sleep(4)  # Wait for both servers
    print("🌐 Opening browser...")
    webbrowser.open('http://localhost:8000')

if __name__ == '__main__':
    print("=" * 60)
    print("🎯 AI Keyword Classifier - Standalone Version")
    print("=" * 60)
    
    try:
        # Start backend in daemon thread
        backend_thread = threading.Thread(target=start_backend, daemon=True)
        backend_thread.start()
        
        # Start browser opener in daemon thread
        browser_thread = threading.Thread(target=open_browser, daemon=True)
        browser_thread.start()
        
        # Start frontend in main thread (this blocks)
        start_frontend()
        
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")
        sys.exit(1)
