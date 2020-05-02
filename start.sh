#!/bin/sh

set -e

createsuperuser () {
    local username="$1"
    local email="$2"
    local password="$3"
    cat <<EOF | python manage.py shell
from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(username="$username").exists():
    User.objects.create_superuser("$username", "$email", "$password")
else:
    print('User "{}" exists already, not created'.format("$username"))
EOF
}

until nc -zv "db" "3306"; do
  echo "Mysql is unavailable - sleeping"
  sleep 1
done

echo "Mysql is up - executing on"

python3 manage.py makemigrations
python3 manage.py migrate
createsuperuser "admin" "lol@kek.os" "www12345"
python3 manage.py runserver 0.0.0.0:8000
