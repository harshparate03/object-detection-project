#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate --fake-initial --noinput

# Download YOLO model if not exists
if [ ! -f "yolov8n.pt" ]; then
    echo "Downloading YOLOv8 model..."
    python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
fi
