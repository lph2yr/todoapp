release: python manage.py migrate
worker: celery -A personaldashboard worker --pool=solo --without-mingle -l info
beat: celery -A personaldashboard beat -l info
web: gunicorn personaldashboard.wsgi