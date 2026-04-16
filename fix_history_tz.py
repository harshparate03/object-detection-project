with open('vision/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix history view - image is now base64 TextField, no .url needed
content = content.replace(
    "'image_url': upload.image.url,",
    "'image_url': upload.image if upload.image else '',"
)

with open('vision/views.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("views.py fixed")

# Fix timezone to IST
with open('object_detection/settings.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("TIME_ZONE = 'UTC'", "TIME_ZONE = 'Asia/Kolkata'")
content = content.replace("USE_TZ = True", "USE_TZ = True  # IST timestamps")

with open('object_detection/settings.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("settings.py timezone fixed to Asia/Kolkata (IST)")
