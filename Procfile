web: gunicorn project.wsgi:application
worker: celery -A project worker -l info
release: python manage.py migrate