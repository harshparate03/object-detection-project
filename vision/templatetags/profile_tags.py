from django import template
from django.conf import settings
import os

register = template.Library()

@register.simple_tag
def profile_image_url(user):
    """
    Safely return profile image URL or default image.
    Works on both local and Render (ephemeral storage).
    """
    try:
        if user.profile_image and user.profile_image.name:
            return user.profile_image.url
    except Exception:
        pass
    # Return default image using STATIC_URL
    return settings.STATIC_URL + 'images/default.jpg'
