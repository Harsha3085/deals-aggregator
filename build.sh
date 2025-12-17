#!/usr/bin/env bash
set -o errexit

echo "=== Starting build process ==="
pip install -r requirements.txt
python manage.py collectstatic --noinput

# Run migrations
python run_migrations.py

# RESET ADMIN PASSWORD (ONE-TIME)
echo "=== Resetting admin password ==="
python reset_admin.py

echo "=== Build completed successfully ==="