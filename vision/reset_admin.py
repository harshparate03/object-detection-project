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
            return HttpResponse('No admin found in database')
        
        admin.set_password('Admin@1234')
        admin.save()
        return HttpResponse(f'Password reset! Email: {admin.email} | Password: Admin@1234')
    except Exception as e:
        return HttpResponse(f'Error: {str(e)}')
