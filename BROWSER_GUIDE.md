# 🌐 How to Open the App in Any Browser

The keyword classifier is a web application that runs in your browser. Here's how to open it properly in **any browser** (Chrome, Firefox, Edge, Safari, etc.):

## Method 1: Using Python's Built-in Server (Recommended)

This works in ALL browsers and avoids CORS issues:

### Windows (PowerShell):
```powershell
cd "C:\path\to\Keyword Classifier\frontend"
python -m http.server 8000
```

### Windows (Command Prompt):
```cmd
cd "C:\path\to\Keyword Classifier\frontend"
python -m http.server 8000
```

### Mac/Linux:
```bash
cd /path/to/Keyword\ Classifier/frontend
python3 -m http.server 8000
```

Then open your browser and go to:
```
http://localhost:8000
```

**✅ Works in:** Chrome, Firefox, Edge, Safari, Opera, Brave, any modern browser!

---

## Method 2: Direct File Opening (Chrome/Edge Only)

This method works but ONLY in Chrome and Edge due to browser security restrictions:

### Windows:
1. Right-click `index.html`
2. Choose "Open with" → Choose your browser

### The Problem:
- **Chrome/Edge**: ✅ Works
- **Firefox**: ❌ Blocks local file access
- **Safari**: ❌ Strict security policies
- **Others**: ❌ May not work

**That's why Method 1 is recommended!**

---

## Full Setup Instructions

### Step 1: Start Ollama
```bash
ollama serve
```
Keep this terminal open.

### Step 2: Start Backend
Open a NEW terminal:
```bash
cd backend
python app.py
```
Keep this terminal open too.

### Step 3: Start Frontend
Open a THIRD terminal:
```bash
cd frontend
python -m http.server 8000
```

### Step 4: Open Browser
Go to: `http://localhost:8000`

---

## Troubleshooting

**Q: "System Status" shows backend offline?**
- Make sure you ran `python app.py` in the backend folder
- Check if port 5000 is in use: try `http://localhost:5000/api/health` in browser

**Q: "Ollama Offline" even though it's running?**
- Make sure you ran `ollama serve`
- Check if port 11434 is in use: try `http://localhost:11434` in browser
- Try pulling the model again: `ollama pull llama3.1:8b`

**Q: Page loads but status shows "Backend Offline"?**
- The frontend loaded but can't reach the backend
- Make sure backend is running on port 5000
- Check firewall isn't blocking local connections

**Q: Works in Chrome but not Firefox?**
- You're probably double-clicking `index.html` (Method 2)
- Use Method 1 instead (Python server)

**Q: "Failed to fetch" errors?**
- Backend isn't running
- Wrong port (should be 5000 for backend, 8000 for frontend)
- CORS issue (use Python server method)

---

## Why Use a Local Server?

Modern browsers have security restrictions that prevent local HTML files from making network requests (called CORS policy). Running a local server:

✅ Avoids CORS issues  
✅ Works in ALL browsers  
✅ Mimics real hosting environment  
✅ Allows proper debugging  

It's the professional way to develop web apps!

---

## One-Line Startup (Advanced)

Want to start everything at once? Create a startup script:

### Windows (PowerShell) - `start-all.ps1`:
```powershell
# Start Ollama (if not auto-running)
Start-Process powershell -ArgumentList "ollama serve"

# Start Backend
Start-Process powershell -ArgumentList "cd backend; python app.py"

# Start Frontend
Start-Process powershell -ArgumentList "cd frontend; python -m http.server 8000"

# Open browser
Start-Sleep -Seconds 3
Start-Process "http://localhost:8000"
```

Run with: `powershell -ExecutionPolicy Bypass -File start-all.ps1`

### Mac/Linux - `start-all.sh`:
```bash
#!/bin/bash

# Start Ollama
ollama serve &

# Start Backend
cd backend && python app.py &

# Start Frontend
cd frontend && python3 -m http.server 8000 &

# Wait a bit then open browser
sleep 3
open http://localhost:8000  # Mac
# OR
xdg-open http://localhost:8000  # Linux
```

Run with: `bash start-all.sh`

---

## Need Help?

1. Check all three terminals are running
2. Visit `http://localhost:5000/api/health` - should show Ollama status
3. Visit `http://localhost:8000` - should show the app
4. Check browser console (F12) for errors
5. Check backend terminal for error messages

**Now your friends can use it in ANY browser!** 🚀
