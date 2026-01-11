"""
Quick script to fix the frontend HTML - replace TWO prompts with ONE
"""
import re

# Read the file
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the two-prompt section
# Pattern: from "<!-- Prompt Editors -->" to the end of second prompt div
pattern = r'<!-- Prompt Editors -->.*?</div>\s*</div>\s*</div>'

replacement = '''<!-- Combined Classification Prompt (ONE PROMPT DOES BOTH!) -->
                    <div class="form-group">
                        <label>
                            AI Classification Prompt (Relevance + Category)
                            <span class="info-tooltip" title="Single prompt that does BOTH relevance and category in one AI call (2x faster!)">ℹ️</span>
                            <button class="btn-reset" id="resetClassificationPrompt">Reset to Default</button>
                        </label>
                        <textarea id="classificationPrompt" class="textarea-field-code" rows="12"></textarea>
                        <div class="help-box">
                            <p class="help-text"><strong>What this does:</strong> This combined prompt analyzes BOTH relevance and category in a single AI call (2x faster!).</p>
                            <p class="help-text"><strong>Available variables:</strong></p>
                            <ul class="help-list">
                                <li><code>{topic}</code> - Your research topic</li>
                                <li><code>{keyword}</code> - The keyword being analyzed</li>
                                <li><code>{categories}</code> - Your list of categories</li>
                            </ul>
                            <p class="help-text"><strong>⚡ Performance:</strong> Single prompt = 2x faster than old two-step process!</p>
                        </div>
                    </div>
                </div>'''

# Use DOTALL flag to match across newlines
content_fixed = re.sub(pattern, replacement, content, flags=re.DOTALL)

# Write back
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content_fixed)

print("✅ HTML fixed - replaced TWO prompts with ONE combined prompt!")
