import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agro_import.settings')
django.setup()

from inventario.models import Maquinaria

t = Maquinaria.objects.filter(modelo__icontains='TL1404 con Cabina').first()
if t:
    print(f"Modelo: {t.modelo}")
    print(f"imagen: {t.imagen}")
    print(f"nombre_imagen_local: {t.nombre_imagen_local}")
