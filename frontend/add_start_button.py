"""
Fix UI: Add START button after manual input section
"""

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find the closing tag of the Input Keywords section (after manual tab)
manual_tab_end = html.find('</div>', html.find('id="manualTab"'))
section_end = html.find('</section>', manual_tab_end)

# Insert START button before the section closing tag
button_html = '''
                <button id="startBtn" class="btn-primary btn-large">Start Classification</button>
'''

html = html[:section_end] + button_html + html[section_end:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('✅ START button added!')
