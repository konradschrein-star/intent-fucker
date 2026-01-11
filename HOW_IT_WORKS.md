# 🧠 How It Works - Under the Hood

This document explains how the app works in simple terms. Perfect for understanding what's happening behind the scenes!

---

## The Big Picture

```
Your Keywords → AI Analysis → Filtered & Categorized Results
```

The app uses **local AI** (Llama 3.1) to read each keyword like a human would and decide:
1. Is this keyword actually about the topic you care about?
2. What type of search is this? (how-to, comparison, etc.)

---

## The Journey of a Keyword

Let's follow one keyword through the entire process:

**Example keyword:** "ys origin walkthrough"  
**Your topic:** "Ys video game series"

### Step 1: You Upload

You put this keyword in a CSV or type it manually. The frontend (what you see in the browser) sends it to the backend (Python server).

### Step 2: Relevance Check

**The app asks the AI:**
> "Hey Llama, I'm researching 'Ys video game series'. Someone searched for 'ys origin walkthrough'. Is this relevant to my topic?"

**The AI thinks:**
- "Ys Origin" is a game in the Ys series ✓
- "walkthrough" means guide for playing it ✓
- Definitely relevant to "Ys video game series" ✓

**The AI responds:**
```json
{
  "relevant": true,
  "confidence": 95,
  "reason": "Ys Origin is a game in the Ys series, walkthrough clearly indicates game guide content"
}
```

**The app checks:**
- Confidence: 95 ≥ threshold (75) ✓
- **KEYWORD ACCEPTED!**

### Step 3: Category Classification

**The app asks the AI:**
> "This keyword is accepted. What category of search intent is 'ys origin walkthrough'?"

**The AI thinks:**
- Words like "walkthrough" = user wants step-by-step guide
- Not asking "how to" (would be how-to category)
- Not comparing anything (would be comparison)
- Clearly wants a guide = walkthrough category ✓

**The AI responds:**
```json
{
  "category": "walkthrough",
  "confidence": 92,
  "reason": "Keyword explicitly requests a walkthrough, indicating user wants comprehensive step-by-step gameplay guide"
}
```

### Step 4: Save Results

The app saves:
```csv
title,views,views_per_year,relevance_score,relevance_accepted,category,category_confidence,reason
ys origin walkthrough,1500,750,95,TRUE,walkthrough,92,"Relevance: Ys Origin is a game..."
```

### Step 5: Repeat

This happens for EVERY keyword in your list!

---

## Now Let's See a Rejection

**Example keyword:** "yes button tutorial"  
**Your topic:** "Ys video game series"

### Relevance Check

**The app asks the AI:**
> "Is 'yes button tutorial' relevant to 'Ys video game series'?"

**The AI thinks:**
- "yes" sounds like "Ys" but totally different meaning ✗
- "button tutorial" = programming/web development topic ✗
- Nothing to do with Ys video games ✗

**The AI responds:**
```json
{
  "relevant": false,
  "confidence": 15,
  "reason": "Keyword is about yes/no button UI elements in web development, not the Ys game series despite similar pronunciation"
}
```

**The app checks:**
- Confidence: 15 < threshold (75) ✗
- **KEYWORD REJECTED!**

Since it's rejected, we don't even bother categorizing it. It goes straight to the rejected CSV.

---

## The Technology Stack

### Frontend (What You See)
- **HTML** - Structure of the page
- **CSS** - Makes it look beautiful (blue/black/grey theme)
- **JavaScript** - Makes buttons work, shows progress, etc.

### Backend (The Brain)
- **Python** - Programming language
- **Flask** - Web framework (serves the API)
- **Pandas** - Handles CSV files
- **Requests** - Talks to Ollama

### AI Engine
- **Ollama** - Local AI server (like running ChatGPT on your PC)
- **Llama 3.1 8B** - The actual AI model (8 billion parameters!)

---

## How the AI Actually Works

### What is Llama 3.1?

Llama 3.1 is a **large language model** (LLM) - think of it as an AI that's read millions of web pages and learned patterns in human language.

**It understands:**
- Word meanings and context
- Nuances (like "ys" vs "yes")
- Search intent (what people are looking for)
- Categories of information

**It's like having a really smart assistant who:**
- Never gets tired
- Can analyze thousands of keywords
- Understands context super well
- Works completely offline

### Why 8B (8 Billion)?

The "8B" means 8 billion parameters - basically 8 billion tiny "knowledge neurons" in the AI's brain.

**Comparison:**
- **GPT-3**: 175 billion parameters (huge, needs powerful servers)
- **Llama 3.1 8B**: 8 billion (optimized to run on your PC)
- **Llama 3.1 70B**: 70 billion (better accuracy, needs GPU)

We use 8B because it's the sweet spot: great accuracy + runs on normal computers!

### How We Guide the AI

We use **prompts** - specific instructions that tell the AI exactly what to do.

**Example Relevance Prompt:**
```
You are a keyword relevance analyzer. Your task is to determine if a search keyword is relevant to a specific topic.

Topic: Ys video game series
Keyword: "ys origin walkthrough"

Analyze whether someone searching for this keyword is likely looking for information about the topic mentioned above.

Respond ONLY with a JSON object in this exact format:
{"relevant": true/false, "confidence": 0-100, "reason": "brief explanation"}
```

**Why so specific?**
- AI is smart but needs clear instructions
- JSON format makes it easy for code to parse
- We tell it exactly what to output

---

## The Processing Pipeline

Here's what happens when you click "Start Classification":

```
1. FRONTEND: "Hey backend, process these keywords with this topic and settings"
   ↓
2. BACKEND: "Got it! Creating a job..."
   ↓ (Creates background thread)
   
3. FOR EACH KEYWORD:
   ├─ Send relevance prompt to Ollama
   ├─ Ollama: Sends to Llama 3.1 AI
   ├─ AI thinks... (2-5 seconds)
   ├─ AI returns JSON response
   ├─ Parse JSON, extract score
   ├─ Check against threshold
   │  
   ├─ IF ACCEPTED:
   │  ├─ Send category prompt to Ollama
   │  ├─ AI categorizes... (2-5 seconds)
   │  └─ Save with category
   │
   └─ IF REJECTED:
      └─ Save to rejected list
   
4. FRONTEND: Polls every 500ms asking "Are you done yet?"
   ↓
5. BACKEND: "Done! Here are the stats and file paths"
   ↓
6. FRONTEND: Shows results, enables download buttons
```

---

## Why Is It Slow?

**Each keyword takes 2-5 seconds because:**

1. **Sending prompt to AI** - ~0.1 seconds
2. **AI thinking** - ~2-4 seconds (this is the AI actually analyzing)
3. **Parsing response** - ~0.1 seconds
4. **Repeat for category** - Another ~2-4 seconds

**Why not faster?**
- AI needs time to "think" (run calculations)
- We're running it locally (not on powerful cloud servers)
- We do TWO AI calls per keyword (relevance + category)

**Could it be faster?**
- **Yes** with a GPU (can be 5-10x faster)
- **Yes** with batch processing (but less accurate)
- **Yes** with smaller model (but less accurate)

We chose accuracy over speed!

---

## The Confidence Score System

### What Does Confidence Mean?

The AI gives a confidence score (0-100) for each decision:

- **90-100**: "I'm very sure!"
- **70-89**: "Pretty confident"
- **50-69**: "Somewhat sure"
- **30-49**: "Not very confident"
- **0-29**: "Really not sure"

### The Threshold Decision

You set a threshold (default: 75%). This means:

**Threshold = 75%:**
- AI says 95% confident → ACCEPT ✓ (95 ≥ 75)
- AI says 60% confident → REJECT ✗ (60 < 75)

**Why have a threshold?**
- Filters out ambiguous keywords
- You control how strict the filter is
- Higher threshold = safer but more rejections
- Lower threshold = more keywords but some false positives

---

## Privacy & Security

### Where Does Data Go?

**Nowhere!** Everything runs on your computer:

1. Your keywords → Stay on your PC
2. AI analysis → Happens on your PC
3. Results → Saved on your PC

**No external API calls!** (except downloading Ollama initially)

### Could Someone Intercept?

**No**, because:
- Backend runs on `localhost` (your computer only)
- No internet connection needed during processing
- No data transmitted externally

**Best practices:**
- Don't expose port 5000 to the internet
- Don't run with `host='0.0.0.0'` unless you know what you're doing
- Keep your keyword lists private

---

## Common Questions

**Q: Can the AI make mistakes?**  
A: Yes! It's very good but not perfect. That's why we show confidence scores. Check low-confidence keywords manually.

**Q: Why does it need so much setup (Ollama, model download)?**  
A: We run the AI locally for privacy and control. The model file (~4.7GB) is the AI's "brain" - it's big but you only download once!

**Q: Could I use ChatGPT API instead?**  
A: Yes! But then your keywords would go to OpenAI's servers (privacy concern) and cost money per keyword. We chose local for free + private.

**Q: What if I have 100,000 keywords?**  
A: It'll work but take ~5-6 days straight. Consider:
- Running overnight
- Splitting into batches
- Using GPU acceleration
- Using the 70B model with better hardware

**Q: Can I customize the categories?**  
A: Absolutely! Add/remove in the UI. The AI will categorize into whatever categories you define.

---

## Want to Learn More?

Check out:
- `backend/ollama_client.py` - How we talk to Ollama
- `backend/classifier.py` - The classification logic
- `backend/config.py` - Default prompts (see how we instruct the AI)
- `frontend/app.js` - How the UI works

**Everything is commented now so you can understand it!** 🎓
