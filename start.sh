#!/bin/bash

echo "Connecting with PostgreSQL driver..."
while ! nc -z db 5432; do
  sleep 1
done

echo "Database Ready! running migrations with alembic..."
alembic upgrade head

echo "Running minium required tests to start the app"
python -m unittest discover app/tests/unit -v

echo "Starting server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
