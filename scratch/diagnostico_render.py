import urllib.request
import urllib.error

urls = [
    "https://martino-tavol.onrender.com",
    "https://martinoagromaquinarias.com.ar",
    "https://www.martinoagromaquinarias.com.ar"
]

print("Iniciando diagnóstico de conexión a los servidores de Render y Cloudflare...\n")

for url in urls:
    print(f"=========================================")
    print(f"🔍 Verificando: {url}")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=15) as response:
            print(f"✅ ESTADO: {response.getcode()} OK")
            print("👉 DIAGNÓSTICO: El sitio responde perfectamente. No hay errores.")
            
    except urllib.error.HTTPError as e:
        print(f"❌ ERROR HTTP: {e.code} - {e.reason}")
        
        # Leer el contenido de la página de error para adivinar qué falló
        body = e.read().decode('utf-8', errors='ignore')
        
        if e.code in [521, 522, 523, 530, 1000]:
            print("👉 DIAGNÓSTICO CLARO: Error de Cloudflare.")
            print("   Explicación: Cloudflare no puede comunicarse con Render. Suele pasar si Render está apagado o el DNS apunta a un lado incorrecto.")
        elif "Application Error" in body or "render.com" in body.lower():
            print("👉 DIAGNÓSTICO CLARO: Error Interno de Render (Gunicorn crasheó).")
            print("   Explicación: El despliegue terminó, pero al intentar iniciar la app en Python, hubo un fallo fatal (ej. faltan variables de entorno, base de datos caída o dependencias rotas).")
        elif "Django" in body or "Traceback" in body or e.code == 500:
            print("👉 DIAGNÓSTICO CLARO: Error de Código de Django (Pantalla Amarilla).")
            print("   Explicación: Django inició, pero un error en el código, en la base de datos o en un template está rompiendo la vista.")
        else:
            print("👉 DIAGNÓSTICO: Error genérico del servidor.")
            print("   Extracto de la página:")
            print(f"   {body[:250]}...")
            
    except urllib.error.URLError as e:
        print(f"🚨 ERROR DE RED/DNS: {e.reason}")
        print("👉 DIAGNÓSTICO: El dominio no resolvió. Puede que aún se esté propagando o no esté configurado en tu PC.")
    except Exception as e:
        print(f"⚠️ ERROR INESPERADO: {e}")
    
    print("=========================================\n")

print("FIN DEL DIAGNÓSTICO. Por favor, revisa los resultados arriba.")
