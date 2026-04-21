"""
URL configuration for agro_import project.
"""
from django.contrib import admin
# 1. Agregamos 'include' a la importación
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # 2. Conectamos la raíz del sitio con las URLs de tu app 'inventario'
    path('', include('inventario.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
