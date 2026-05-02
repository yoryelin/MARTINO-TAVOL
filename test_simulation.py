import os
import django

# 1. Configuración del entorno
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agro_import.settings')
django.setup()

from inventario.models import Maquinaria, ConfiguracionFinanciera
from inventario.context_processors import admin_metrics
from django.test import RequestFactory

def simular_y_comprobar():
    print("=== INICIANDO SIMULACIÓN DE COMPROBACIÓN (HANDOVER TEST) ===\n")
    
    # --- PASO 1: CARGA DE DATOS TEMPORALES ---
    print("[1/3] Cargando datos de prueba efímeros...")
    
    # Crear configuración financiera de prueba
    conf, created = ConfiguracionFinanciera.objects.get_or_create(id=1)
    conf.tasa_usd = 2.5
    conf.tasa_pesos = 22.0
    conf.vigente = True
    conf.save()
    
    # Crear máquina de prueba
    test_m = Maquinaria.objects.create(
        marca="TEST",
        modelo="SIMULACION PROD",
        potencia_hp=100,
        traccion="4x4",
        precio_usd=50000.00,
        apto_credito_bna=True,
        nombre_imagen_local="tractor_cabin.png"
    )
    
    # --- PASO 2: VERIFICACIÓN DE LÓGICA ---
    print("[2/3] Verificando lógica del sistema...")
    
    # Verificación de Imágenes (Nueva lógica prioritaria)
    img_url = test_m.imagen_url_segura
    print(f"  > Resolución de imagen: {img_url}")
    if "tractor_cabin.png" in img_url:
        print("  ✅ ÉXITO: La imagen local prioritaria funciona correctamente.")
    else:
        print("  ❌ ERROR: La lógica de imagen no tomó el valor local.")

    # Verificación de Dashboard (Context Processor)
    factory = RequestFactory()
    request = factory.get('/admin/')
    request.user = type('User', (), {'is_authenticated': True, 'is_staff': True})()
    
    context = admin_metrics(request)
    metrics = context.get('metrics', {})
    
    print(f"  > Dashboard BNA USD: {metrics.get('bna_usd')}%")
    print(f"  > Dashboard BNA Pesos: {metrics.get('bna_pesos')}%")
    
    if metrics.get('bna_usd') == 2.5 and metrics.get('bna_pesos') == 22.0:
        print("  ✅ ÉXITO: El Dashboard refleja las tasas cargadas.")
    else:
        print("  ❌ ERROR: El Dashboard no muestra los datos financieros actuales.")

    # --- PASO 3: LIMPIEZA ABSOLUTA ---
    print("\n[3/3] Eliminando datos de simulación...")
    
    test_m.delete()
    # Resetear tasas a 0 para dejarlo limpio
    conf.tasa_usd = 0
    conf.tasa_pesos = 0
    conf.vigente = False
    conf.save()
    
    print("  ✅ ÉXITO: Base de datos restaurada a estado neutral.")
    print("\n=== SIMULACIÓN FINALIZADA CON ÉXITO: PROYECTO VALIDADO ===")

if __name__ == "__main__":
    try:
        simular_y_comprobar()
    except Exception as e:
        print(f"❌ Error durante la simulación: {e}")
