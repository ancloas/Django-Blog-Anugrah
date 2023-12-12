# Run Gunicorn with relative path to the parent directory
cd blog_avg
gunicorn blog_avg.wsgi:application -c ../gunicorn_config.py
