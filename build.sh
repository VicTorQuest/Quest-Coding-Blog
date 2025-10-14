#!/bin/bash
python manage.py migrate --noinput

echo "
from django.contrib.auth import get_user_model
import os

User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

if username and email and password:
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
        print('Superuser created.')
    else:
        print('Superuser already exists.')
else:
    print('Superuser environment variables not fully set.')
" | python manage.py shell

python manage.py collectstatic --noinput