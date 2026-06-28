from .models import AccessLog

class AccessLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Es preferible registrar después o antes, lo haremos antes para asegurar que se registre incluso si hay error 500
        # Ignore static and media files
        if not (request.path.startswith('/static/') or request.path.startswith('/media/')):
            # Get IP address
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
                
            user_agent = request.META.get('HTTP_USER_AGENT', '')

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
