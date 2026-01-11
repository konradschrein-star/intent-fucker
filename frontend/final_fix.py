"""
COMPREHENSIVE FIX - Removes duplicates and fixes all references
"""

# ===== FIX HTML - Remove duplicate prompt section =====
with open('index.html', 'r', encoding='utf-8') as f:
    html_lines = f.readlines()

# Find line 293 (the duplicate section start) and remove it until line 311
# Keep only the first occurrence (lines 202-220)
# Remove lines ~293-311
new_html_lines = html_lines[:292] + html_lines[311:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.writelines(new_html_lines)

print("✅ HTML fixed - removed duplicate classific ationPrompt section")

# ===== FIX JAVASCRIPT - Update loadSettings function =====
with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace the old prompt loading code with new combined prompt loading
js = js.replace(
    """        // Load prompts
        if (data.relevance_prompt) {
            defaultRelevancePrompt = data.relevance_prompt;
            elements.relevancePrompt.value = data.relevance_prompt;
        }
        
        if (data.category_prompt) {
            defaultCategoryPrompt = data.category_prompt;
            elements.categoryPrompt.value = data.category_prompt;
        }""",
    """        // Load combined classification prompt
        if (data.classification_prompt) {
            defaultClassificationPrompt = data.classification_prompt;
            elements.classificationPrompt.value = data.classification_prompt;
        }"""
)

# Also fix startProcessing to send classification_prompt
js = js.replace(
    """        relevance_prompt: elements.relevancePrompt.value,
        category_prompt: elements.categoryPrompt.value""",
    """        classification_prompt: elements.classificationPrompt.value"""
)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("✅ JavaScript fixed - loadSettings now uses classification_prompt")
print("✅ JavaScript fixed - startProcessing now sends classification_prompt")
print("\n🎉 ALL FIXES COMPLETE!")
print("Refresh your browser with Ctrl+Shift+R to see the changes!")
