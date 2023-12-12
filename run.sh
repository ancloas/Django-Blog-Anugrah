
# Run runserver
gunicorn your_project_name.wsgi:application -c gunicorn_config.py
