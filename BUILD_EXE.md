# AI Keyword Classifier - Standalone Executable Build

## Installationsanleitung für die .exe

### Voraussetzungen:
1. **Ollama installieren**: https://ollama.ai/download
2. **Llama 3.1 Model herunterladen**:
   ```bash
   ollama pull llama3.1:8b
   ```

### Nutzung:
1. `KeywordClassifier.exe` herunterladen
2. Doppelklick auf die .exe
3. Browser öffnet sich automatisch auf http://localhost:8000
4. Fertig!

## Entwickler-Info: Build-Prozess

### Abhängigkeiten installieren:
```bash
pip install pyinstaller
```

### Executable erstellen:
```bash
python build_exe.py
```

Die .exe wird im `dist/` Ordner erstellt.

### Was ist enthalten:
- Python Backend (Flask Server)
- Alle Frontend-Dateien (HTML, CSS, JS)
- Alle Python-Dependencies
- Auto-Start-Skript (öffnet Browser automatisch)

### Größe:
- Ca. 50-80 MB (inklusive aller Dependencies)
