import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Configure ALLOWED_HOSTS
settings.ALLOWED_HOSTS += ['testserver', 'localhost', '127.0.0.1']

from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse

c = Client()
print("--- Testing Enhanced Signup Flow ---")

# Data for new user
new_user_data = {
    'username': 'newuser_v2',
    'email': 'newuser_v2@example.com',
    'first_name': 'New',
    'last_name': 'User',
    'password': 'password123',
    'confirm_password': 'password123'
}

# 1. Test Signup Page Load
print("\n1. Loading Signup Page...")
response = c.get(reverse('signup'))
if response.status_code == 200:
    print("SUCCESS: Signup page loaded.")
else:
    print(f"FAIL: Signup page status {response.status_code}")

# 2. Test Signup Submission
print("\n2. Submitting Signup Form...")
signup_data = {
    'username': 'newuser_v2',
    'email': 'newuser_v2@example.com',
    'first_name': 'New',
    'last_name': 'User',
    'password1': 'password123',
    'password2': 'password123'
}

# Clean up if exists
if User.objects.filter(username='newuser_v2').exists():
    User.objects.get(username='newuser_v2').delete()

response = c.post(reverse('signup'), signup_data, follow=True)

if response.status_code == 200:
    # Check if user was created
    if User.objects.filter(username='newuser_v2').exists():
        user = User.objects.get(username='newuser_v2')
        print(f"SUCCESS: User '{user.username}' created.")
        print(f"   Name: {user.get_full_name()}")
        print(f"   Email: {user.email}")
        
        if user.first_name == 'New' and user.email == 'newuser_v2@example.com':
            print("SUCCESS: First Name and Email saved correctly.")
        else:
            print("FAIL: Data mismatch.")
    else:
        print("FAIL: User not created.")
        if response.context and 'form' in response.context:
            print(f"Validation Errors: {response.context['form'].errors}")
        else:
            print("Form not found in context or context is None.")
            print("Response Content Start:")
            print(response.content.decode('utf-8')[:500])
else:
    print(f"FAIL: Submission returned {response.status_code}")
