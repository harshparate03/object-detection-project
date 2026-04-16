with open('vision/models.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    "    image = models.ImageField(upload_to='upload_history/')",
    "    image = models.TextField(blank=True, null=True)  # base64 data URL"
)

with open('vision/models.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("models.py fixed")

# Fix upload_image view - store annotated image as base64 in DB instead of file
with open('vision/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the UploadHistory.objects.create in upload_image view
old = """            from .models import UploadHistory
            from django.utils.timezone import now
            output_name = f"annotated_{uploaded_file.name}"
            try:
                default_storage.save(output_name, ContentFile(out_buffer.tobytes()))
            except Exception:
                pass
            UploadHistory.objects.create(
                user=request.user,
                image=output_name,
                detected_objects=str(detected_objects),
                uploaded_at=now()
            )"""

new = """            from .models import UploadHistory
            from django.utils.timezone import now
            import base64 as _b64
            annotated_b64 = "data:image/jpeg;base64," + _b64.b64encode(out_buffer.tobytes()).decode('utf-8')
            UploadHistory.objects.create(
                user=request.user,
                image=annotated_b64,
                detected_objects=str(detected_objects),
                uploaded_at=now()
            )"""

if old in content:
    content = content.replace(old, new)
    print("upload_image view fixed")
else:
    print("Pattern not found in upload_image - trying alternate fix")
    # fallback: replace just the image=output_name line
    content = content.replace(
        "                image=output_name,",
        '                image="data:image/jpeg;base64," + __import__("base64").b64encode(out_buffer.tobytes()).decode("utf-8"),'
    )
    # remove the default_storage.save block
    content = content.replace(
        """            output_name = f"annotated_{uploaded_file.name}"
            try:
                default_storage.save(output_name, ContentFile(out_buffer.tobytes()))
            except Exception:
                pass
""", "")
    print("Fallback fix applied")

# Fix admin_history view - image is now base64 text, no .url needed
content = content.replace(
    "'image_url': upload.image.url if upload.image and hasattr(upload.image, 'url') else '',",
    "'image_url': upload.image if upload.image else '',"
)
# also fix the original if it wasn't patched before
content = content.replace(
    "'image_url': upload.image.url,",
    "'image_url': upload.image if upload.image else '',"
)

# Fix delete_upload_history - no more .path on image
content = content.replace(
    """    try:
        if upload.image:
            image_path = upload.image.path
            if os.path.exists(image_path):
                os.remove(image_path)  # Delete the image file from the system
        upload.delete()  # Delete the record from the database
        messages.success(request, "Upload history entry deleted successfully.")
    except Exception as e:
        messages.error(request, f"An error occurred while deleting the history entry: {e}")""",
    """    try:
        upload.delete()
        messages.success(request, "Upload history entry deleted successfully.")
    except Exception as e:
        messages.error(request, f"An error occurred while deleting the history entry: {e}")"""
)

# Fix admin_delete_history - no more .path on image
content = content.replace(
    """    try:
        if history_item.image:
            image_path = history_item.image.path
            if os.path.exists(image_path):
                os.remove(image_path)
        history_item.delete()
        messages.success(request, "History entry deleted successfully.")
    except Exception as e:
        messages.error(request, f"An error occurred while deleting the history entry: {e}")""",
    """    try:
        history_item.delete()
        messages.success(request, "History entry deleted successfully.")
    except Exception as e:
        messages.error(request, f"An error occurred while deleting the history entry: {e}")"""
)

with open('vision/views.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("views.py fixed")
