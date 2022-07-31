web: gunicorn run:app
worker: celery -A app.tasks worker --loglevel=info