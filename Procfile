web: python manage.py migrate && python manage.py collectstatic --noinput && gunicorn junkbusters.wsgi --bind 0.0.0.0:$PORT --workers 2
