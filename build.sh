#!/usr/bin/env bash
# exit on error
set -o errexit

# Instalar dependencias
pip install -r requirements.txt

# Recopilar archivos estáticos
python manage.py collectstatic --no-input

# Aplicar migraciones
python manage.py migrate

# Cargar catálogo de maquinaria (Seed)
python seed_martino_tavol.py

# Configurar roles y permisos (RBAC)
python setup_roles.py

# Crear superusuario automáticamente
python create_admin.py
