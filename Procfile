release: python manage.py migrate
web: gunicorn greatkart.wsgi:application --bind 0.0.0.0:$PORT