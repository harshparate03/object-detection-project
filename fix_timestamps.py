with open('vision/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix history view - format uploaded_at in IST
content = content.replace(
    "            'uploaded_at': upload.uploaded_at,\n            'username': upload.user.username",
    "            'uploaded_at': upload.uploaded_at.strftime('%d %b %Y, %I:%M %p IST'),\n            'username': upload.user.username"
)

# Fix admin_history view - already uses strftime but UTC, update format
content = content.replace(
    "'uploaded_at': upload.uploaded_at.strftime('%Y-%m-%d %H:%M:%S'),  # Directly using uploaded_at",
    "'uploaded_at': upload.uploaded_at.strftime('%d %b %Y, %I:%M %p IST'),"
)

with open('vision/views.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Timestamps fixed to IST format")
