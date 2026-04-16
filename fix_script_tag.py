with open('vision/templates/dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the duplicate <script> tag
content = content.replace(
    '                    <!-- handle video upload -->\n                    <script>\n\n                    <script>',
    '                    <!-- handle video upload -->\n                    <script>'
)

with open('vision/templates/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed duplicate script tag")
