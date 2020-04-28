#!/bin/sh
# start.sh

set -e
  
host="db"

until PGPASSWORD="postgres" psql -h "$host" -U "postgres" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done
  
>&2 echo "Postgres is up - executing command"
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser --username "admin" --email "lol@kek.os" --noinput
python3 manage.py runserver 0.0.0.0:8000


