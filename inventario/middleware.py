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

            # Save to AccessLog
            try:
                AccessLog.objects.create(
                    ip_address=ip,
                    path=request.path,
                    user_agent=user_agent
                )
            except Exception:
                pass # Failsafe to not break the site if DB is locked
        
        response = self.get_response(request)
        return response
