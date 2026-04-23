import os
import shutil
from pathlib import Path

def organizar():
    # Rutas
    base_dir = Path(r'c:\Users\Estudiante\Desktop\MARTINO')
    # Ruta interna donde Gemini guardó las imágenes (la extraigo de mis logs)
    brain_dir = Path(r'C:\Users\Estudiante\.gemini\antigravity\brain\cf8d93b5-ad7d-430b-886a-1a90aa860024')
    
    static_img_dir = base_dir / 'inventario' / 'static' / 'inventario' / 'img' / 'tractores'
    
    # Crear carpeta si no existe
    static_img_dir.mkdir(parents=True, exist_ok=True)
    
    mapeo = {
        'tractor_greenhouse': 'tractor_greenhouse.png',
        'tractor_standard': 'tractor_standard.png',
        'tractor_cabin': 'tractor_cabin.png',
        'tractor_dual': 'tractor_dual.png',
        'tractor_loader': 'tractor_loader.png'
    }
    
    print(f"Buscando imágenes en {brain_dir}...")
    
    encontrados = 0
    # Buscamos en la carpeta brain_dir
    if brain_dir.exists():
        for archivo_path in brain_dir.glob('tractor_*.png'):
            for clave, nombre_final in mapeo.items():
                if clave in archivo_path.name:
                    destino = static_img_dir / nombre_final
                    shutil.copy2(archivo_path, destino)
                    print(f"  [OK] Copiado: {archivo_path.name} -> {destino}")
                    encontrados += 1
    
    if encontrados == 0:
        print("  [!] No se pudieron copiar las imágenes. Por favor, asegúrate de que el script tenga acceso a la ruta.")
    else:
        print(f"\nSe organizaron {encontrados} imágenes con éxito en la carpeta static.")

if __name__ == '__main__':
    organizar()
