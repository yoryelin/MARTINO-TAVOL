import os
import shutil
from pathlib import Path

def organizar():
    # Rutas
    base_dir = Path(__file__).resolve().parent
    static_img_dir = base_dir / 'inventario' / 'static' / 'inventario' / 'img' / 'tractores'
    
    # Crear carpeta si no existe
    static_img_dir.mkdir(parents=True, exist_ok=True)
    
    # Lista de archivos generados (basado en los nombres que gemini guardó)
    # Buscamos los archivos que empiezan con 'tractor_' en el directorio raíz
    archivos_generados = list(base_dir.glob('tractor_*.png'))
    
    mapeo = {
        'tractor_greenhouse': 'tractor_greenhouse.png',
        'tractor_standard': 'tractor_standard.png',
        'tractor_cabin': 'tractor_cabin.png',
        'tractor_dual': 'tractor_dual.png',
        'tractor_loader': 'tractor_loader.png'
    }
    
    print(f"Buscando imágenes en {base_dir}...")
    
    encontrados = 0
    for archivo in archivos_generados:
        for clave, nombre_final in mapeo.items():
            if clave in archivo.name:
                destino = static_img_dir / nombre_final
                shutil.copy2(archivo, destino)
                print(f"  [OK] Copiado: {archivo.name} -> {destino}")
                encontrados += 1
    
    if encontrados == 0:
        print("  [!] No se encontraron las imágenes generadas. Asegúrate de que estén en la carpeta raíz del proyecto.")
    else:
        print(f"\nSe organizaron {encontrados} imágenes con éxito.")

if __name__ == '__main__':
    organizar()
