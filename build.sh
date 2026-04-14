#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate --fake-initial --noinput

# Download YOLOv3 weights at build time (better accuracy than tiny)
if [ ! -f "yolov3.weights" ]; then
    echo "Downloading YOLOv3 weights..."
    curl -L -o yolov3.weights https://pjreddie.com/media/files/yolov3.weights
fi

if [ ! -f "yolov3.cfg" ]; then
    echo "Downloading YOLOv3 config..."
    curl -L -o yolov3.cfg https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3.cfg
fi

if [ ! -f "coco.names" ]; then
    echo "Downloading COCO names..."
    curl -L -o coco.names https://raw.githubusercontent.com/pjreddie/darknet/master/data/coco.names
fi
