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

from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from inventario.sitemaps import StaticViewSitemap, MaquinariaSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'maquinaria': MaquinariaSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    # 2. Conectamos la raíz del sitio con las URLs de tu app 'inventario'
    path('', include('inventario.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name="inventario/robots.txt", content_type="text/plain")),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
