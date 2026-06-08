#!/bin/bash
set -e

echo "Running database migrations..."
flask db upgrade

echo "Seeding database..."
python seed.py

echo "Starting application..."
exec flask run --host=0.0.0.0 --port=5023
