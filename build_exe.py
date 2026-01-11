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

# Build arguments (Windows syntax uses ; for paths)
args = [
    'launcher.py',  # Main entry point
    '--name=KeywordClassifier',
    '--onefile',  # Single executable
    '--windowed',  # No console window
    '--add-data=frontend;frontend',  # Include frontend files (Windows: semicolon!)
    '--add-data=backend;backend',  # Include backend files
    '--hidden-import=flask',
    '--hidden-import=flask_cors',
    '--hidden-import=pandas',
    '--hidden-import=requests',
    '--hidden-import=dotenv',
    '--clean',
]

# Run PyInstaller
PyInstaller.__main__.run(args)

print("\n" + "=" * 60)
print("✅ Build Complete!")
print("=" * 60)

exe_path = 'dist/KeywordClassifier.exe'
if os.path.exists(exe_path):
    size_mb = os.path.getsize(exe_path) / 1024 / 1024
    print(f"📦 Executable location: {exe_path}")
    print(f"📏 File size: {size_mb:.1f} MB")
    print("\n🚀 Ready to distribute!")
else:
    print("❌ Build failed - executable not found")
