with open('vision/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix history view - properly convert UTC to IST (+5:30)
content = content.replace(
    "            'uploaded_at': upload.uploaded_at.strftime('%d %b %Y, %I:%M %p IST'),",
    "            'uploaded_at': (upload.uploaded_at + __import__('datetime').timedelta(hours=5, minutes=30)).strftime('%d %b %Y, %I:%M %p') + ' IST',"
)

# Fix admin_history view
content = content.replace(
    "'uploaded_at': upload.uploaded_at.strftime('%d %b %Y, %I:%M %p IST'),",
    "'uploaded_at': (upload.uploaded_at + __import__('datetime').timedelta(hours=5, minutes=30)).strftime('%d %b %Y, %I:%M %p') + ' IST',"
)

with open('vision/views.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done - UTC to IST conversion fixed")
