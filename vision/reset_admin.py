from django.http import HttpResponse
from vision.models import UserProfile
from django.contrib.auth.hashers import make_password

def reset_admin_password(request):
    secret = request.GET.get('secret', '')
    if secret != 'vision_reset_2024':
        return HttpResponse('Unauthorized', status=403)

    email = request.GET.get('email', 'admin@gmail.com')
    new_pass = request.GET.get('password', 'Admin@1234')

    try:
        user = UserProfile.objects.filter(email=email).first()
        if not user:
            user = UserProfile.objects.filter(role='admin').first()
        if not user:
            return HttpResponse('No user found')

        user.set_password(new_pass)
        user.save()
        return HttpResponse(f'Password updated! Email: {user.email} | New Password: {new_pass}')
    except Exception as e:
        return HttpResponse(f'Error: {str(e)}')
