#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate --fake-initial --noinput

# Create media directories for file uploads
mkdir -p media/profile_images
mkdir -p media/uploads
mkdir -p media/output-videos

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
