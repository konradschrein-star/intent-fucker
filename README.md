# 🎯 AI Keyword Classifier

**Intelligente Keyword-Analyse mit Llama 3.1 AI**

Klassifiziere und filtere Keywords automatisch nach Relevanz und Such-Intent. Perfekt für SEO, Content-Strategien und Keyword-Research.

---

## 📥 Download & Installation

### Option 1: Standalone .exe (Empfohlen für Nicht-Entwickler)

**1. Voraussetzung: Ollama installieren**
- Download: https://ollama.ai/download
- Model herunterladen: `ollama pull llama3.1:8b`

**2. App herunterladen**
- [KeywordClassifier.exe](https://github.com/konradschrein-star/intent-fucker/releases/latest) herunterladen
- Doppelklick auf die .exe
- Browser öffnet sich automatisch → Fertig! 🎉

### Option 2: Von Source ausführen (Entwickler)

**Voraussetzungen:**
- Python 3.8+
- Ollama mit llama3.1:8b Model

**Installation:**
```bash
# Repository klonen
git clone https://github.com/konradschrein-star/intent-fucker.git
cd intent-fucker

# Backend Dependencies installieren
cd backend
pip install -r requirements.txt

# Backend starten
python app.py

# In neuem Terminal: Frontend starten
cd ../frontend
python -m http.server 8000

# Browser öffnen: http://localhost:8000
```

---

## ✨ Features

- **🤖 KI-basierte Klassifizierung** - Llama 3.1 analysiert Keywords intelligent
- **⚡ 2x Schneller** - Kombinierter Prompt für Relevanz + Kategorie in einem Schritt
- **📊 CSV Upload & Export** - Massenverarbeitung von Keywords
- **🎨 Interaktive UI** - Live-Console, Zeit-Schätzung, Fortschrittsanzeige
- **⚙️ Vollständig konfigurierbar** - Eigene Kategorien, Prompts und Schwellenwerte
- **🔒 100% Lokal** - Alle Daten bleiben auf deinem Rechner

### Kategorien (anpassbar):
- **how-to** - Schritt-für-Schritt Anleitungen
- **comparison** - Reviews, Tests, Vergleiche
- **walkthrough** - Umfassende Übersichten (längere, tiefere Videos)
- **informational** - Allgemeine Informationssuche
- **transactional** - Kaufabsicht / Downloads

---

## 🚀 Nutzung

1. **Topic eingeben** - Dein Thema/Produkt (z.B. "Ys Videospiele")
2. **Keywords hochladen** - CSV mit Keywords oder manuell eingeben
3. **Settings anpassen** (optional) - Schwellenwert, Kategorien, Prompts
4. **Start drücken** - AI analysiert Keywords
5. **Ergebnisse herunterladen** - Accepted + Rejected CSVs

### CSV Format:
```csv
title,views,views_per_year
ys origin walkthrough,50000,25000
best ys games,30000,15000
```

---

## 🏗️ Eigene .exe bauen

```bash
# PyInstaller installieren
pip install pyinstaller

# Build Script ausführen
python build_exe.py

# Executable in dist/ Ordner
```

---

## 🛠️ Technologie

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python (Flask, Pandas)
- **AI Model:** Llama 3.1 8B (via Ollama)

---

## 📝 Lizenz

Privates Projekt von Konrad Schrein.

**Wer Code klaut kriegt Dünnschiss.** 💩

---

## 🐛 Troubleshooting

**Backend Offline?**
- `python backend/app.py` ausführen
- Port 5000 frei?

**Ollama Offline?**
- `ollama serve` ausführen
- `ollama pull llama3.1:8b` für Model

**Prompt lädt nicht?**
- Hard Refresh: `Ctrl + Shift + R`
- Console checken (F12)

---

**Made with ❤️ for Keyword Analysis | Powered by Llama 3.1**
