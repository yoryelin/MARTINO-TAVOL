import urllib.request
import os

url = "https://logo.clearbit.com/bna.com.ar"
save_path = os.path.join("inventario", "static", "inventario", "img", "bna_logo.png")

try:
    print("Descargando logo de Banco Nación...")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        with open(save_path, 'wb') as f:
            f.write(response.read())
    print("¡Logo descargado con éxito en:", save_path, "!")
except Exception as e:
    print("Error descargando:", e)
