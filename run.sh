
# Run runserver
gunicorn blog_avg.wsgi:application -c gunicorn_config.py
