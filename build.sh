#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate --fake-initial --noinput

# Download YOLOv3-tiny weights at build time
if [ ! -f "yolov3-tiny.weights" ]; then
    echo "Downloading YOLOv3-tiny weights..."
    curl -L -o yolov3-tiny.weights https://pjreddie.com/media/files/yolov3-tiny.weights
fi

if [ ! -f "yolov3-tiny.cfg" ]; then
    echo "Downloading YOLOv3-tiny config..."
    curl -L -o yolov3-tiny.cfg https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3-tiny.cfg
fi
