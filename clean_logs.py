import os
import django

# Configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agro_import.settings')
django.setup()

from inventario.models import AccessLog, IPCache

def clean_logs():
    print("--- INICIANDO LIMPIEZA DE BÓVEDA DE INTELIGENCIA ---")
    
    # 1. Eliminar todos los logs de acceso
    access_deleted, _ = AccessLog.objects.all().delete()
    print(f"[OK] Eliminados {access_deleted} registros de AccessLog.")
    
    # 2. Eliminar todas las IPs cacheadas
    ip_deleted, _ = IPCache.objects.all().delete()
    print(f"[OK] Eliminadas {ip_deleted} IPs cacheadas.")

    print("\n--- LIMPIEZA COMPLETADA CON ÉXITO ---")

if __name__ == '__main__':
    clean_logs()
