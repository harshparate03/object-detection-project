from django.contrib import admin
from .models import UserProfile  # Assuming you have a model for the users

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'email', 'phone', 'status', 'role', 'is_active')
    list_filter = ('status', 'role', 'is_active')
    search_fields = ('username', 'name', 'email', 'phone')
    readonly_fields = ('email', 'phone')  # Prevents accidental changes

admin.site.register(UserProfile, UserProfileAdmin)

