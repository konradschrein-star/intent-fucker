# 🚀 Quick Start Guide - Keyword Classifier

## Prerequisites Check

✅ Python installed
✅ Project files created
⚠️ **Ollama needs to be installed**

## Step 1: Install Ollama

1. **Download Ollama for Windows**:
   - Visit: https://ollama.ai/download
   - Download the Windows installer
   - Run the installer

2. **Verify Installation**:
   ```powershell
   ollama --version
   ```

3. **Pull Llama 3.1 Model**:
   ```powershell
   ollama pull llama3.1:8b
   ```
   This will download ~4.7GB (may take a few minutes)

4. **Start Ollama Service** (if not auto-started):
   ```powershell
   ollama serve
   ```
   Keep this terminal open while using the app.

## Step 2: Install Python Dependencies

The dependencies are being installed automatically. If you need to install manually:

```powershell
cd "c:\Users\konra\OneDrive\YouTube\Projekte\YTA Tutorials\Programs\Keyword Classifier\backend"
pip install -r requirements.txt
```

## Step 3: Start the Application

### Terminal 1: Backend Server
```powershell
cd "c:\Users\konra\OneDrive\YouTube\Projekte\YTA Tutorials\Programs\Keyword Classifier\backend"
python app.py
```

Backend will run on: `http://localhost:5000`

### Terminal 2: Frontend Server
```powershell
cd "c:\Users\konra\OneDrive\YouTube\Projekte\YTA Tutorials\Programs\Keyword Classifier\frontend"
python -m http.server 8000
```

Frontend will run on: `http://localhost:8000`

**OR** you can simply open `frontend/index.html` directly in your browser.

## Step 4: Test the Application

1. Open browser to `http://localhost:8000` (or open `index.html`)
2. Check that "Ollama Status" shows "Online" in the header
3. Enter a topic: `Ys video game series`
4. Upload the `sample_keywords.csv` file
5. Click "Start Classification"
6. Watch the progress bar!
7. Download the results

## Sample Test Keywords

I've created a `sample_keywords.csv` file with test data:
- Mix of relevant keywords (ys games)
- Irrelevant keywords (yes/no, html tutorials)
- Various categories (walkthrough, review, comparison, etc.)

Perfect for testing the classifier!

## Troubleshooting

### "Ollama Offline" status
- Make sure Ollama is installed
- Run `ollama serve` in a terminal
- Check firewall isn't blocking port 11434

### "Backend Offline" status
- Make sure backend is running: `python app.py`
- Check port 5000 is not in use

### Model not found
- Pull the model: `ollama pull llama3.1:8b`
- Check available models: `ollama list`

### Slow processing
- Llama 3.1 8B is optimized for local use
- Each keyword takes ~2-5 seconds
- For large batches (100+ keywords), expect several minutes

## Next Steps

✨ **Your keyword classifier is ready!**

Try it out with the sample file, then use your own CSV data for:
- YouTube keyword research
- SEO keyword filtering
- Content categorization
- Search intent analysis

Enjoy! 🎉
