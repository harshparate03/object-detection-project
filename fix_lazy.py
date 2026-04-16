import re

# Fix header.html - change lazy to eager for profile images
with open('vision/templates/includes/header.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Logo image - keep lazy (not critical)
# Profile images - change to eager since they're small base64 or small files
content = content.replace(
    '<img alt="User" width="920" height="920" style="color:transparent"',
    '<img alt="User" width="40" height="40" style="color:transparent; width:40px; height:40px; object-fit:cover; border-radius:50%;"'
)
content = content.replace(
    '<img alt="User Images" width="920" height="920" data-nimg="1"\n                                                style="color:transparent"',
    '<img alt="User Images" width="50" height="50" data-nimg="1"\n                                                style="color:transparent; width:50px; height:50px; object-fit:cover; border-radius:50%;"'
)

with open('vision/templates/includes/header.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("header.html fixed")
