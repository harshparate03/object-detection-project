web: python manage.py migrate && python manage.py collectstatic --noinput && gunicorn object_detection.wsgi:application --bind 0.0.0.0:$PORT
