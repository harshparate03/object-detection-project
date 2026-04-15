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
            admin = UserProfile(
                username='admin',
                email='admin@gmail.com',
                name='Admin',
                phone='0000000000',
                role='admin',
                is_superuser=True,
                is_staff=True
            )
            admin.set_password('Admin@1234')
            admin.save()
            return HttpResponse('Admin created! Email: admin@gmail.com | Password: Admin@1234')
        
        admin.set_password('Admin@1234')
        admin.save()
        return HttpResponse(f'Password reset! Email: {admin.email} | Password: Admin@1234')
    except Exception as e:
        return HttpResponse(f'Error: {str(e)}')
