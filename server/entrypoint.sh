#!/bin/sh
if [ "$DATABASE" = "postgres"]; then
    echo "Waitng for postgres..."

    while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
    sleep 0.1
    done

    echo "PostgresSQL started" 
fi

# Make migration and migrate the database.
echo "Making migration and migrating the database"

python manage.py make migrations main --noinput
python manage.py migrate --noinput
exec "$@"