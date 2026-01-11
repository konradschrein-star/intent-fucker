"""
Quick script to fix the frontend - replace TWO prompts with ONE combined prompt
"""

# Read the HTML file
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find and replace the two-prompt section with one combined prompt
old_section_start = html.find('<!-- Prompt Editors -->')
old_section_end = html.find('</div>\n                </div>\n            </section>', old_section_start)

new_prompt_section = '''<!-- Combined Classification Prompt -->
                    <div class="form-group">
                        <label>
                            AI Classification Prompt (Relevance + Category)
                            <span class="info-tooltip" title="Single prompt that does BOTH relevance and category in one AI call (2x faster!)">ℹ️</span>
                            <button class="btn-reset" id="resetClassificationPrompt">Reset to Default</button>
                        </label>
                        <textarea id="classificationPrompt" class="textarea-field-code" rows="14"></textarea>
                        <div class="help-box">
                            <p class="help-text"><strong>What this does:</strong> ONE prompt that analyzes BOTH relevance AND category in a single AI call (2x faster!).</p>
                            <p class="help-text"><strong>Variables you can use:</strong></p>
                            <ul class="help-list">
                                <li><code>{topic}</code> - Your research topic</li>
                                <li><code>{keyword}</code> - The keyword being analyzed</li>
                                <li><code>{categories}</code> - Your list of categories</li>
                            </ul>
                            <p class="help-text"><strong>⚡ Why it's better:</strong> Old system: 2 AI calls = SLOW. New system: 1 AI call = 2X FASTER!</p>
                            <p class="help-text"><strong>💡 Advanced users:</strong> Must return JSON: <code>{"relevant": true/false, "relevance_confidence": 0-100, "category": "name", "category_confidence": 0-100}</code></p>
                        </div>
                    </div>
                </div>'''

html_new = html[:old_section_start] + new_prompt_section + html[old_section_end:]

# Write the updated HTML
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_new)

print("✅ HTML updated - TWO prompts replaced with ONE combined prompt")

# Now fix the JavaScript
with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Update DOM elements
js = js.replace(
    "relevancePrompt: document.getElementById('relevancePrompt'),\n    categoryPrompt: document.getElementById('categoryPrompt'),\n    resetRelevancePrompt: document.getElementById('resetRelevancePrompt'),\n    resetCategoryPrompt: document.getElementById('resetCategoryPrompt'),",
    "classificationPrompt: document.getElementById('classificationPrompt'),\n    resetClassificationPrompt: document.getElementById('resetClassificationPrompt'),"
)

# Update state variables
js = js.replace(
    "// Default AI prompts (loaded from backend, can be edited by users)\nlet defaultRelevancePrompt = '';  // Prompt for checking if keyword is relevant\nlet defaultCategoryPrompt = '';   // Prompt for categorizing keywords",
    "// Default AI prompt (loaded from backend, can be edited by users)\nlet defaultClassificationPrompt = '';  // Combined prompt for relevance + category"
)

# Update loadSettings function
old_load = '''        // Load prompts
        if (data.relevance_prompt) {
            defaultRelevancePrompt = data.relevance_prompt;
            elements.relevancePrompt.value = data.relevance_prompt;
        }
        
        if (data.category_prompt) {
            defaultCategoryPrompt = data.category_prompt;
            elements.categoryPrompt.value = data.category_prompt;
        }'''

new_load = '''        // Load combined classification prompt
        if (data.classification_prompt) {
            defaultClassificationPrompt = data.classification_prompt;
            elements.classificationPrompt.value = data.classification_prompt;
        }'''

js = js.replace(old_load, new_load)

# Update event listeners
old_listeners = '''    elements.resetRelevancePrompt.addEventListener('click', () => {
        elements.relevancePrompt.value = defaultRelevancePrompt;
    });
    elements.resetCategoryPrompt.addEventListener('click', () => {
        elements.categoryPrompt.value = defaultCategoryPrompt;
    });'''

new_listeners = '''    elements.resetClassificationPrompt.addEventListener('click', () => {
        elements.classificationPrompt.value = defaultClassificationPrompt;
    });'''

js = js.replace(old_listeners, new_listeners)

# Update startProcessing to send classification_prompt
old_request = '''    const requestData = {
        topic,
        confidence_threshold: parseInt(elements.confidenceSlider.value),
        categories,
        relevance_prompt: elements.relevancePrompt.value,
        category_prompt: elements.categoryPrompt.value
    };'''

new_request = '''    const requestData = {
        topic,
        confidence_threshold: parseInt(elements.confidenceSlider.value),
        categories,
        classification_prompt: elements.classificationPrompt.value
    };'''

js = js.replace(old_request, new_request)

# Write updated JavaScript
with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("✅ JavaScript updated - now uses ONE combined prompt")
print("\n🎉 Frontend integration complete!")
print("Refresh your browser to see the changes!")
