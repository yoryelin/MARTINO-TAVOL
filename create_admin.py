import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agro_import.settings')
django.setup()

from django.contrib.auth.models import User

# Datos del administrador
username = 'admin'
email = 'nicolas@martinoagromaquinarias.com.ar'
password = 'MartinoAdmin2024'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f"Superuser {username} created successfully.")
else:
    print(f"Superuser {username} already exists.")
