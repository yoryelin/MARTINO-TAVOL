import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agro_import.settings')
django.setup()

from inventario.models import Maquinaria, ConfiguracionFinanciera

try:
    # 1. Asegurar que exista una configuración financiera activa
    financiacion, created = ConfiguracionFinanciera.objects.get_or_create(id=1)
    financiacion.vigente = True
    financiacion.tasa_usd = 0
    financiacion.tasa_pesos = 19
    financiacion.plazo_meses = 60
    financiacion.save()
    print("- Configuración financiera asegurada y vigente.")

    # 2. Buscar el tractor TL1404 con Cabina y ponerle precio
    tractor = Maquinaria.objects.filter(modelo__icontains='TL1404 con Cabina').first()
    if tractor:
        tractor.precio_usd = 48798.00
        tractor.apto_credito_bna = True
        tractor.save()
        print(f"- ¡Éxito! Precio de USD 48,798.00 aplicado al tractor: {tractor.modelo}")
    else:
        print("- Error: No se encontró el tractor TL1404 con Cabina en la base de datos.")

except Exception as e:
    print(f"Error: {e}")
