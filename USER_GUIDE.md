# 📖 User Guide for Intent Fucker

## What Does This App Do?

Imagine you have a list of 1,000 search keywords, but half of them are totally irrelevant to what you're researching. **This app uses AI to automatically:**

1. **Filter out irrelevant keywords** - Remove the junk
2. **Categorize the good ones** - Organize by search intent (how-to, comparison, etc.)
3. **Export clean data** - Get organized CSV files ready to use

### Real Example

You're researching the "Ys" video game series for YouTube content planning:

**Your messy keyword list:**
- ys origin walkthrough ✅ (relevant - it's about Ys games)
- ys 8 gameplay ✅ (relevant)
- yes button tutorial ❌ (not relevant - different "yes")
- ys vs trails comparison ✅ (relevant)
- yes or no javascript ❌ (not relevant)

**App filters it automatically:**
- ✅ **Accepted**: 3 keywords about Ys games
- ❌ **Rejected**: 2 keywords about "yes/no" (different topic)

Plus it categorizes the good ones:
- "ys origin walkthrough" → **walkthrough** category
- "ys 8 gameplay" → **informational** category  
- "ys vs trails comparison" → **comparison** category

---

## Step-by-Step Guide

### 1️⃣ First Time Setup

#### Install Ollama (The AI Engine)

1. **Download Ollama**: Go to https://ollama.ai/download
2. **Install it**: Run the installer (just like any program)
3. **Open Terminal/PowerShell** and type:
   ```bash
   ollama pull llama3.1:8b
   ```
   This downloads the AI model (~4.7GB). It only needs to be done once!

4. **Start Ollama** (if it didn't auto-start):
   ```bash
   ollama serve
   ```
   Keep this window open while using the app.

#### Install Python Dependencies

1. **Open Terminal/PowerShell**
2. **Navigate to the backend folder**:
   ```bash
   cd "path/to/Keyword Classifier/backend"
   ```
3. **Install requirements**:
   ```bash
   pip install -r requirements.txt
   ```

---

### 2️⃣ Starting the App

Every time you want to use the app:

#### Start the Backend (The Brain)

1. Open Terminal/PowerShell
2. Navigate to backend folder:
   ```bash
   cd "path/to/Keyword Classifier/backend"
   ```
3. Start the server:
   ```bash
   python app.py
   ```
4. You should see: `Running on http://localhost:5000`
5. **Keep this window open!**

#### Open the Frontend (The Interface)

1. Navigate to the `frontend` folder
2. **Option A - Simple**: Just double-click `index.html`
3. **Option B - Better**: Run a local server:
   ```bash
   cd frontend
   python -m http.server 8000
   ```
   Then open browser to `http://localhost:8000`

---

### 3️⃣ Using the App

#### Check Status

- Look at top-right corner
- Should say **"Ollama Online"** with a green dot
- If it says "Offline", make sure Ollama is running (`ollama serve`)

#### Enter Your Topic

In the "Topic / Target Subject" box, type what your keywords should be about.

**Examples:**
- "Ys video game series"
- "iPhone 15 reviews"
- "Python programming tutorials"
- "Vegan recipes"

**Be specific!** The AI uses this to judge if keywords are relevant.

#### Add Your Keywords

**Option 1 - Upload CSV File:**

1. Click or drag-drop a CSV file into the upload area
2. Your CSV must have these columns:
   - `title` - The keyword/search term
   - `views` - Number of views
   - `views_per_year` - Views per year
3. Example CSV format:
   ```csv
   title,views,views_per_year
   ys origin walkthrough,1500,750
   ys 8 gameplay,2000,1000
   ```

**Option 2 - Manual Input:**

1. Click the "Manual Input" tab
2. Type/paste keywords (one per line)
3. Format options:
   - Simple: `ys origin walkthrough`
   - With data: `ys origin walkthrough,1500,750`

#### Adjust Settings (Optional)

Click **"Expand"** to customize:

**Confidence Threshold:**
- Slider from 0% to 100%
- **Default: 75%** - Only accept keywords the AI is 75%+ sure about
- **Lower** (50%) = More keywords accepted (but more false positives)
- **Higher** (90%) = Only very confident matches (safer but stricter)

**Categories:**
- Default: how-to, comparison, walkthrough, informational, transactional
- **Add custom**: Type new category name and click "Add"
- **Remove**: Click ✕ on any category pill

**Edit Prompts (Advanced):**
- Click "Relevance Filter Prompt" or "Category Classification Prompt"
- Modify how the AI analyzes keywords
- Click "Reset to Default" if you mess up

#### Start Processing

1. Click the big blue **"Start Classification"** button
2. Watch the progress bar! It shows:
   - Current keyword being processed
   - Progress (X / Total)
   - Percentage complete
3. **Time estimate**: ~2-5 seconds per keyword
   - 10 keywords = ~30 seconds
   - 100 keywords = ~5 minutes
   - 1000 keywords = ~50 minutes

#### Download Results

When processing completes, you'll see:

**Statistics:**
- Total keywords processed
- How many accepted
- How many rejected
- Acceptance rate

**Category Breakdown:**
- Visual bars showing distribution
- How many keywords in each category

**Download Buttons:**
1. **Download Accepted Keywords** - The good stuff! 
   - Format: `accepted_keywords_20260111_215930.csv`
   - Contains all relevant keywords with categories
2. **Download Rejected Keywords** - The filtered junk
   - Format: `rejected_keywords_20260111_215930.csv`
   - See what was removed and why

---

## Understanding the Output Files

### Accepted Keywords CSV

Contains these columns:

| Column | Description | Example |
|--------|-------------|---------|
| `title` | The keyword | "ys origin walkthrough" |
| `views` | Total views | 1500 |
| `views_per_year` | Views per year | 750 |
| `relevance_score` | AI confidence (0-100) | 95 |
| `relevance_accepted` | Passed threshold? | TRUE |
| `category` | Search intent type | "walkthrough" |
| `category_confidence` | Category confidence | 88 |
| `reason` | AI's explanation | "Relevance: Directly about Ys game walkthrough..." |

### Rejected Keywords CSV

Same columns, but `relevance_accepted` = FALSE

Use the `reason` column to understand why keywords were rejected!

---

## Tips & Best Practices

### 🎯 Writing Good Topics

**Good:**
- "Ys video game series"
- "iPhone 15 Pro Max reviews"
- "Vegan baking recipes"

**Bad (too vague):**
- "games" (too broad)
- "phone" (which phone?)
- "food" (too general)

### ⚡ Performance Tips

- **First keyword is slowest** (~5-10 seconds) while AI "warms up"
- **Subsequent keywords are faster** (~2-3 seconds each)
- **Don't close the terminal** running the backend!
- **Don't close browser tab** during processing

### 🔧 Troubleshooting

**"Backend Offline" status:**
- Make sure you ran `python app.py` in backend folder
- Check port 5000 isn't used by another app

**"Ollama Offline" status:**
- Run `ollama serve` in terminal
- Check Ollama installed correctly: `ollama --version`

**Processing stuck at 0%:**
- Check backend terminal for errors
- Make sure Llama model is downloaded: `ollama list`

**Slow processing:**
- Normal! Each keyword takes 2-5 seconds
- Llama 3.1 8B is optimized for local use
- For faster processing, use GPU if available

**All keywords rejected:**
- Check your topic is specific enough
- Lower the confidence threshold (try 50-60%)
- Look at `reason` column to see why

**Weird categories:**
- Edit the "Category Classification Prompt"
- Make sure your custom categories make sense
- Reset to defaults if confused

---

## FAQ

**Q: Do I need internet?**
A: No! After downloading Ollama and the model, everything runs offline. Your keywords never leave your computer.

**Q: Can I process multiple files?**
A: Yes! Just upload a new file after the first completes, or merge CSVs before uploading.

**Q: How accurate is it?**
A: Very good for clear cases. Llama 3.1 understands context well. Check the `confidence_score` - anything above 80 is usually accurate.

**Q: Can I use different AI models?**
A: Yes! Edit `backend/config.py` to change `OLLAMA_MODEL`. Try `llama3.1:70b` for better accuracy (but slower).

**Q: What if I have 10,000 keywords?**
A: It'll work, but take ~5-8 hours. Consider splitting into batches or running overnight.

**Q: Can I run this on a server?**
A: Yes! It's built with Flask. Just change `host='0.0.0.0'` in app.py and open port 5000.

**Q: Is my data private?**
A: 100%! Everything runs locally. No data sent to external APIs.

---

## Example Workflow

Here's a complete example from start to finish:

**Goal:** Find relevant keywords for YouTube videos about the Ys game series

1. **Start services**
   - Terminal 1: `ollama serve`
   - Terminal 2: `python backend/app.py`
   - Browser: Open `frontend/index.html`

2. **Setup**
   - Topic: "Ys video game series"
   - Upload `my_keywords.csv` with 100 keywords
   - Confidence: 75% (default)
   - Categories: Keep defaults

3. **Process**
   - Click "Start Classification"
   - Wait ~5 minutes
   - See results: 67 accepted, 33 rejected

4. **Review**
   - Check category breakdown
   - Download accepted keywords
   - Use for YouTube content planning!

5. **Refine (if needed)**
   - Look at rejected keywords
   - Maybe some were incorrectly filtered?
   - Lower threshold to 65% and re-run

---

## Need Help?

- Check `README.md` for technical details
- Check `QUICK_START.md` for setup instructions
- Read error messages in backend terminal
- Look at the `reason` column in output CSVs

**Happy keyword filtering!** 🎉
