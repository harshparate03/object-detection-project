from django import template
from django.templatetags.static import static

register = template.Library()

@register.simple_tag
def profile_image_url(user):
    """Safely return profile image URL or default image"""
    try:
        if user.profile_image and user.profile_image.name:
            return user.profile_image.url
    except Exception:
        pass
    return static('images/default.jpg')
