#!/bin/bash

# Activate the virtual environment (if you are using one)
# source /path/to/your/virtualenv/bin/activate

# Run makemigrations
python blog_avg/manage.py makemigrations

# Run migrate
python blog_avg/manage.py migrate

# Run runserver
python blog_avg/manage.py runserver
