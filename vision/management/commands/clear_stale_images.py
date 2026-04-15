from django.core.management.base import BaseCommand
from vision.models import UserProfile
import os


class Command(BaseCommand):
    help = 'Clear stale profile image DB references where file no longer exists on disk'

    def handle(self, *args, **kwargs):
        cleared = 0
        for user in UserProfile.objects.exclude(profile_image='').exclude(profile_image=None):
            try:
                path = user.profile_image.path
                if not os.path.exists(path):
                    user.profile_image = None
                    user.save(update_fields=['profile_image'])
                    self.stdout.write(f'Cleared stale image for: {user.username}')
                    cleared += 1
            except Exception:
                user.profile_image = None
                user.save(update_fields=['profile_image'])
                self.stdout.write(f'Cleared broken image for: {user.username}')
                cleared += 1
        self.stdout.write(self.style.SUCCESS(f'Done. Cleared {cleared} stale profile image(s).'))
