import re

with open('vision/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix edit_user view - replace everything between def edit_user and the next blank line after return
old_pattern = r"(def edit_user\(request, user_id\):.*?return render\(request, 'edit_user\.html', \{'form': form, 'edit_user': user\}\))"
new_func = """def edit_user(request, user_id):
    user = get_object_or_404(UserProfile, id=user_id, role="user")

    if request.method == 'POST':
        form = CustomUserForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            if 'profile_image' in request.FILES:
                import base64
                img = request.FILES['profile_image']
                img_data = base64.b64encode(img.read()).decode('utf-8')
                user.profile_image = f"data:{img.content_type};base64,{img_data}"
            user.save()
            messages.success(request, 'User updated successfully!')
            return redirect('admin_dashboard')
    else:
        form = CustomUserForm(instance=user)

    return render(request, 'edit_user.html', {'form': form, 'edit_user': user})"""

new_content = re.sub(old_pattern, new_func, content, flags=re.DOTALL)

# Fix admin_history view - replace image_url to handle missing files gracefully
old_history = r"(def admin_history\(request\):.*?'image_url': upload\.image\.url,)"
new_history_url = r"\1"

# Replace upload.image.url with safe fallback
new_content = new_content.replace(
    "'image_url': upload.image.url,",
    "'image_url': upload.image.url if upload.image and hasattr(upload.image, 'url') else '',"
)

# Fix generate_report - profile_image.path no longer valid (it's base64 now)
new_content = new_content.replace(
    "profile_image_path = user.profile_image.path if user.profile_image else None",
    "profile_image_path = None  # profile_image is now base64 text, not a file path"
)

with open('vision/views.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Done!")
