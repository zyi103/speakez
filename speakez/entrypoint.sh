#!/bin/sh

python manage.py migrate
python manage.py collecstatic

uwsgi --ini uwsgi.ini