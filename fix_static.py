with open('object_detection/settings.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the duplicate assets directory
content = content.replace(
    "    os.path.join(BASE_DIR, 'vision', 'templates', 'assets'),",
    ""
)

with open('object_detection/settings.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done - removed duplicate STATICFILES_DIRS entry")
