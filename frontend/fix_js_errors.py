"""Fix the remaining JavaScript errors"""
import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Fix the loadSettings function - remove old prompt loading
old_pattern = r'''        // Load prompts
        if \(data\.relevance_prompt\) \{
            defaultRelevancePrompt = data\.relevance_prompt;
            elements\.relevancePrompt\.value = data\.relevance_prompt;
        \}
        
        if \(data\.category_prompt\) \{
            defaultCategoryPrompt = data\.category_prompt;
            elements\.categoryPrompt\.value = data\.category_prompt;
        \}'''

new_code = '''        // Load combined classification prompt
        if (data.classification_prompt) {
            defaultClassificationPrompt = data.classification_prompt;
            elements.classificationPrompt.value = data.classification_prompt;
        }'''

js = re.sub(old_pattern, new_code, js, flags=re.MULTILINE)

# Also update the startProcessing to send classification_prompt
old_request_pattern = r'''        relevance_prompt: elements\.relevancePrompt\.value,
        category_prompt: elements\.categoryPrompt\.value'''

new_request = '''        classification_prompt: elements.classificationPrompt.value'''

js = re.sub(old_request_pattern, new_request, js)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("✅ JavaScript fixed!")
print("- loadSettings now uses classification_prompt")
print("- startProcessing now sends classification_prompt")
print("\nRefresh your browser!")
