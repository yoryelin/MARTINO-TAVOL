from .models import AccessLog

class AccessLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Es preferible registrar después o antes, lo haremos antes para asegurar que se registre incluso si hay error 500
        # Ignore static and media files
        if not (request.path.startswith('/static/') or request.path.startswith('/media/')):
            
            # MODO FANTASMA: Si la cookie secreta está presente, ignoramos el registro.
            if request.COOKIES.get('is_developer_sartori') == 'true':
                return self.get_response(request)

            # Get IP address
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
                
            user_agent = request.META.get('HTTP_USER_AGENT', '')

            # Módulo Secreto: Geolocalización (Cache)
            try:
                from .models import IPCache
                if ip and not IPCache.objects.filter(ip_address=ip).exists():
                    import urllib.request
                    import json
                    try:
                        url = f"http://ip-api.com/json/{ip}"
                        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                        with urllib.request.urlopen(req, timeout=1.5) as response:
                            data = json.loads(response.read().decode())
                            if data.get('status') == 'success':
                                IPCache.objects.create(
                                    ip_address=ip,
                                    ciudad=data.get('city'),
                                    provincia_estado=data.get('regionName'),
                                    pais=data.get('country')
                                )
                            else:
                                IPCache.objects.create(ip_address=ip)
                    except Exception:
                        IPCache.objects.create(ip_address=ip)
            except Exception:
                pass

            # --- FILTROS ANTI-BASURA ---
            is_valid_traffic = True
            
            # 1. Filtro Anti-Bots
            ua_lower = user_agent.lower()
            bots_keywords = ['bot', 'spider', 'crawl', 'slurp', 'headless', 'dataprovider']
            if any(keyword in ua_lower for keyword in bots_keywords):
                is_valid_traffic = False
            
            # 2. Filtro de País (Solo Argentina)
            if is_valid_traffic and ip:
                try:
                    from .models import IPCache
                    cached_ip = IPCache.objects.filter(ip_address=ip).first()
                    # Solo permitimos el registro si el país es explícitamente Argentina
                    if not cached_ip or cached_ip.pais != 'Argentina':
                        is_valid_traffic = False
                except Exception:
                    is_valid_traffic = False

            # Save to AccessLog SOLO si es tráfico válido y argentino
            if is_valid_traffic:
                try:
                    AccessLog.objects.create(
                        ip_address=ip,
                        path=request.path,
                        user_agent=user_agent
                    )
                except Exception:
                    pass # Failsafe to not break the site if DB is locked
        
        response = self.get_response(request)

        # MÓDULO SECRETO: Rastrear a Martino
        # Si es una ruta del sistema y el usuario está autenticado, pero NO tiene la cookie de desarrollador
        if request.path.startswith('/sistema-martino/') or request.path.startswith('/admin/'):
            if hasattr(request, 'user') and request.user.is_authenticated:
                if request.COOKIES.get('is_developer_sartori') != 'true':
                    try:
                        from .models import ActividadAdministrador
                        
                        # Definir acción basada en la ruta o método
                        accion = "Navegación"
                        if request.method == "POST":
                            accion = "Guardó datos o realizó una acción (POST)"
                        elif request.method == "GET":
                            # Intentar traducir la ruta a algo legible
                            if "consulta" in request.path:
                                accion = "Revisó Consultas"
                            elif "maquinaria" in request.path:
                                accion = "Revisó Catálogo"
                            elif "accesslog" in request.path:
                                accion = "Revisó Estadísticas"
                            elif request.path == "/sistema-martino/":
                                accion = "Entró al Inicio del Panel"
                            else:
                                accion = f"Visitó: {request.path}"
                                
                        ActividadAdministrador.objects.create(
                            accion=accion,
                            path=request.path
                        )
                    except Exception:
                        pass

        return response
