release: python manage.py migrate
worker: python manage.py celery -A personaldashboard worker --pool=solo --without-mingle -l info
web: gunicorn personaldashboard.wsgi