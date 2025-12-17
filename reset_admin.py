#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'deals_project.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Try to get the 'admin' user, or create it if it doesn't exist
try:
    admin_user = User.objects.get(username='admin')
    print(f"✅ Found existing admin user. Resetting password...")
except User.DoesNotExist:
    print("⚠️  Admin user not found. Creating a new one...")
    admin_user = User.objects.create_superuser(
        username='sriharsha3085',
        email='harsha211091@gmail.com',
        password='harsha_deals'  # You'll change this immediately
    )

# Set the new password (change 'YourNewPassword123!' to your desired password)
admin_user.set_password('harsha_deals')
admin_user.save()

print("=" * 50)
print("SUPERUSER CREDENTIALS HAVE BEEN UPDATED")
print("=" * 50)
print(f"Username: admin")
print(f"Password: YourNewPassword123!")
print("=" * 50)
print("⚠️  IMPORTANT: Log in and change this password immediately!")
print("Also, remove this script after deployment.")
