web: gunicorn wsgi:app
celeryworker: celery -A app.blueprints.contact.tasks worker --loglevel=info -E