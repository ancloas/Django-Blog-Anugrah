#!/bin/bash

# Activate the virtual environment (if you are using one)
# source /path/to/your/virtualenv/bin/activate

#install requirements.txt
pip install -r requirements.txt

# collect static
python blog_avg/manage.py collectstatic --no-input

# Run makemigrations
python blog_avg/manage.py makemigrations

# Run migrate
python blog_avg/manage.py migrate

# Add super user
if [[ $CREATE_SUPERUSER ]];
then
  python blog_avg/manage.py createsuperuser --no-input
fi
