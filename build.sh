#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Ensure static directory exists
mkdir -p static

python manage.py collectstatic --no-input
python manage.py migrate
python manage.py ensure_admin
python manage.py seed_database
