from django import template
from django.templatetags.static import static
import os

register = template.Library()

@register.simple_tag
def profile_image_url(user):
    """
    Safely return profile image URL.
    Falls back to default.jpg if:
    - No profile image set
    - File doesn't exist on disk (Render ephemeral storage)
    - Any other error
    """
    try:
        if user.profile_image and user.profile_image.name:
            # Check if file actually exists on disk
            try:
                path = user.profile_image.path
                if os.path.exists(path):
                    return user.profile_image.url
            except Exception:
                # On Render, path may not be accessible - try URL directly
                return user.profile_image.url
    except Exception:
        pass
    return static('images/default.jpg')
