from django.http import HttpResponse
from vision.models import UserProfile

def reset_admin_password(request):
    """Temporary view to reset admin password on Render - remove after use"""
    secret = request.GET.get('secret', '')
    if secret != 'vision_reset_2024':
        return HttpResponse('Unauthorized', status=403)
    
    try:
        admin = UserProfile.objects.filter(role='admin').first()
        if not admin:
            # Create admin if doesn't exist
            admin = UserProfile.objects.create_superuser(
                username='admin',
                email='admin@gmail.com',
                password='Admin@1234'
            )
            admin.role = 'admin'
            admin.save()
            return HttpResponse(f'Admin created: email=admin@gmail.com password=Admin@1234')
        
        admin.set_password('Admin@1234')
        admin.save()
        return HttpResponse(f'Password reset! Email: {admin.email} | Password: Admin@1234')
    except Exception as e:
        return HttpResponse(f'Error: {str(e)}')
