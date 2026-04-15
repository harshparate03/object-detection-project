#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate --fake-initial --noinput

# Clear stale profile image DB references (Render ephemeral filesystem wipes files on deploy)
python manage.py shell -c "
from vision.models import UserProfile
import os
for u in UserProfile.objects.exclude(profile_image='').exclude(profile_image=None):
    try:
        if not os.path.exists(u.profile_image.path):
            u.profile_image = None
            u.save(update_fields=['profile_image'])
            print(f'Cleared stale image for user: {u.username}')
    except Exception:
        u.profile_image = None
        u.save(update_fields=['profile_image'])
        print(f'Cleared broken image for user: {u.username}')
"

# Download YOLOv3-tiny weights at build time
if [ ! -f "yolov3-tiny.weights" ]; then
    echo "Downloading YOLOv3-tiny weights..."
    curl -L -o yolov3-tiny.weights https://pjreddie.com/media/files/yolov3-tiny.weights
fi

if [ ! -f "yolov3-tiny.cfg" ]; then
    echo "Downloading YOLOv3-tiny config..."
    curl -L -o yolov3-tiny.cfg https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3-tiny.cfg
fi

if [ ! -f "coco.names" ]; then
    echo "Downloading COCO names..."
    curl -L -o coco.names https://raw.githubusercontent.com/pjreddie/darknet/master/data/coco.names
fi
