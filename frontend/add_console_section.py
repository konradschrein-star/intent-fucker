"""
Complete HTML fix: Add ALL missing elements that JavaScript expects
"""

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find where to insert processing console (after Start button, before Settings)
start_btn_pos = html.find('Start Classification</button>')
settings_section_pos = html.find('<!-- Settings Section -->', start_btn_pos)

# Insert Processing Console section
console_html = '''

            <!-- Processing Console Section -->
            <section class="card console-section" id="consoleSection" style="display: none;">
                <h2 class="section-title">
                    Processing Console
                </h2>
                
                <div class="console-header">
                    <div class="console-status">
                        <span id="progressStatus">Ready</span>
                    </div>
                    <div class="console-stats">
                        <span id="progressCount">0 / 0</span>
                        <span id="progressPercentage">0%</span>
                    </div>
                </div>
                
                <div class="progress-container" id="progressContainer">
                    <div class="progress-bar">
                        <div class="progress-fill" id="progressFill"></div>
                    </div>
                    <div class="time-estimate" id="timeEstimate"></div>
                </div>
                
                <div class="console-window">
                    <div class="console-controls">
                        <span class="console-badge" id="consoleBadge">0 keywords</span>
                        <button class="btn-console-toggle" id="consoleToggle">
                            <span>Show Details</span>
                        </button>
                    </div>
                    <div class="console-output" id="consoleOutput"></div>
                </div>
            </section>
'''

html = html[:settings_section_pos] + console_html + html[settings_section_pos:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('✅ Processing Console section added!')
