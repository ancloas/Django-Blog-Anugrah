
# Run runserver
cd blog_avg
gunicorn blog_avg.wsgi:application -c gunicorn_config.py
