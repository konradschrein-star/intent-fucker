"""
Build Script for Creating Standalone Windows Executable
Creates a single .exe file that contains everything needed to run the app
"""

import PyInstaller.__main__
import os
import shutil

print("=" * 60)
print("🔨 Building Keyword Classifier Standalone Executable")
print("=" * 60)

# Clean previous builds
if os.path.exists('build'):
    shutil.rmtree('build')
if os.path.exists('dist'):
    shutil.rmtree('dist')

# PyInstaller arguments
PyInstaller.__main__.run([
    'launcher.py',  # Main entry point
    '--name=KeywordClassifier',
    '--onefile',  # Single executable
    '--windowed',  # No console window
    '--icon=icon.ico' if os.path.exists('icon.ico') else '',
    '--add-data=frontend;frontend',  # Include frontend files
    '--add-data=backend;backend',  # Include backend files  
    '--hidden-import=flask',
    '--hidden-import=flask_cors',
    '--hidden-import=pandas',
    '--hidden-import=requests',
    '--hidden-import=dotenv',
    '--clean',
])

print("\n" + "=" * 60)
print("✅ Build Complete!")
print("=" * 60)
print(f"📦 Executable location: dist/KeywordClassifier.exe")
print(f"📏 File size: {os.path.getsize('dist/KeywordClassifier.exe') / 1024 / 1024:.1f} MB")
print("\n🚀 Ready to distribute!")
