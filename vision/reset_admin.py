from django.http import HttpResponse
from vision.models import UserProfile
from django.contrib.auth.hashers import make_password

def reset_admin_password(request):
    secret = request.GET.get('secret', '')
    if secret != 'vision_reset_2024':
        return HttpResponse('Unauthorized', status=403)
    
    try:
        admin = UserProfile.objects.filter(role='admin').first()
        if not admin:
            # Get field names to know what's available
            fields = [f.name for f in UserProfile._meta.get_fields()]
            # Create admin with minimal required fields
            admin = UserProfile()
            admin.username = 'admin'
            admin.email = 'admin@gmail.com'
            admin.role = 'admin'
            admin.is_superuser = True
            admin.is_active = True
            # Set optional fields if they exist
            if 'name' in fields:
                admin.name = 'Admin'
            if 'phone' in fields:
                admin.phone = '0000000000'
            admin.set_password('Admin@1234')
            admin.save()
            return HttpResponse(f'Admin created! Email: admin@gmail.com | Password: Admin@1234 | Fields: {fields}')
        
        admin.set_password('Admin@1234')
        admin.save()
        return HttpResponse(f'Password reset! Email: {admin.email} | Password: Admin@1234')
    except Exception as e:
        return HttpResponse(f'Error: {str(e)}')
