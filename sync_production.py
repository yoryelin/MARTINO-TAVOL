import os
import django
from django.core.files import File
from pathlib import Path

# Configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agro_import.settings')
django.setup()

from inventario.models import Maquinaria, ConfiguracionFinanciera

def run_sync():
    print("--- INICIANDO SINCRONIZACIÓN DE CATÁLOGO ---")
    
    # 1. Limpiar datos existentes en Producción (Opcional, pero recomendado para evitar duplicados)
    Maquinaria.objects.all().delete()
    ConfiguracionFinanciera.objects.all().delete()
    print("[OK] Base de datos de producción limpia.")

    # 2. Configuración Financiera BNA (Default)
    ConfiguracionFinanciera.objects.create(
        tasa_usd=1.50,
        tasa_pesos=25.00,
        plazo_meses=60,
        vigente=True
    )
    print("[OK] Tasas BNA configuradas.")

    # 3. Lista de Maquinaria extraída de Local
    maquinas_data = [
        ('TAVOL', 'TL304 Invernadero', 30, 'disponible', True),
        ('TAVOL', 'TL504 Invernadero', 50, 'transito', True),
        ('TAVOL', 'TL704 Invernadero', 70, 'pedido', True),
        ('TAVOL', 'TL504', 50, 'disponible', True),
        ('TAVOL', 'TL504 con Cabina', 50, 'disponible', True),
        ('TAVOL', 'TL704', 70, 'transito', True),
        ('TAVOL', 'TL704 con Cabina', 70, 'disponible', True),
        ('TAVOL', 'TL904 con Cabina', 90, 'pedido', True),
        ('TAVOL', 'TL1004 con Cabina', 100, 'disponible', True),
        ('TAVOL', 'TL1404 con Cabina', 140, 'pedido', True),
        ('TAVOL', 'TL1804 con Cabina y Duales', 180, 'pedido', True),
        ('TAVOL', 'TL704 con Cabina y Pala Frontal', 70, 'transito', True),
        ('TAVOL', 'TL1004 con Cabina y Pala Frontal', 100, 'pedido', True)
    ]

    # Carpeta de imágenes estáticas en el servidor
    base_static_path = Path('inventario/static/inventario/img/tractores')

    for marca, modelo, hp, stock, bna in maquinas_data:
        # Determinar imagen base
        img_name = 'tractor_standard.png'
        if 'Invernadero' in modelo:
            img_name = 'tractor_greenhouse.png'
        elif 'Duales' in modelo:
            img_name = 'tractor_dual.png'
        elif 'Pala' in modelo:
            img_name = 'tractor_loader.png'
        elif 'Cabina' in modelo:
            img_name = 'tractor_cabin.png'
        
        img_path = base_static_path / img_name
        
        # Crear la máquina
        maquina = Maquinaria(
            marca=marca,
            modelo=modelo,
            potencia_hp=hp,
            traccion='4x4', # Default para TAVOL
            motor='YTO / Weichai',
            transmision='Sincronizada',
            estado_stock=stock,
            apto_credito_bna=bna,
            descripcion=f"Tractor {marca} {modelo} de {hp} HP. Tecnología de alta performance para el campo argentino.",
            especificaciones_extra="Tracción: 4x4\nTipo: Agrícola\nSoporte: MARTINO Agromaquinarias"
        )
        
        # Subir imagen a Cloudinary si existe el archivo local
        if img_path.exists():
            with open(img_path, 'rb') as f:
                maquina.imagen.save(img_name, File(f), save=False)
        
        maquina.save()
        print(f"  [+] Sincronizado: {modelo} ({hp} HP) - Imagen: {img_name}")

    print("\n--- SINCRONIZACIÓN COMPLETADA CON ÉXITO ---")
    print("Ya puedes revisar el catálogo en la web y el panel de administración.")

if __name__ == '__main__':
    run_sync()
