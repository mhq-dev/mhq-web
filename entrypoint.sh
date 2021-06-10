#!/bin/sh

#python manage.py flush --no-input

while ! python manage.py migrate --no-input 2>&1; do
   echo "Migration is in progress status"
   sleep 3
done

while ! python manage.py collectstatic --no-input 2>&1; do
   echo "Collect static is in progress status"
   sleep 3
done

exec "$@"
