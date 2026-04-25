"""
URL configuration for agro_import project.
"""
from django.contrib import admin
# 1. Agregamos 'include' a la importación
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.urls import re_path
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    # 2. Conectamos la raíz del sitio con las URLs de tu app 'inventario'
    path('', include('inventario.urls')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
