#!/bin/bash

set -e

echo "Waiting for PostgreSQL..."

until pg_isready -h postgres -p 5432 -U ubun -d postdatabase; do
    sleep 2
done

echo "PostgreSQL is ready."

echo "Waiting for Redis..."

until python -c "import socket; s=socket.create_connection(('redis',6379),2); s.close()"; do
    sleep 2
done

echo "Redis is ready."

echo "Running migrations..."

python manage.py migrate

echo "Starting Django..."

exec python manage.py runserver 0.0.0.0:8000