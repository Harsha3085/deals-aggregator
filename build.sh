#!/usr/bin/env bash
# build.sh
set -o errexit

echo "=== Starting build process ==="

# Install Python packages
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# RUN MIGRATIONS AUTOMATICALLY
echo "=== Running database migrations ==="
python run_migrations.py

echo "=== Build completed successfully ==="