from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Maquinaria

class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = 'weekly'

    def items(self):
        return ['home', 'catalogo']

    def location(self, item):
        return reverse(item)

class MaquinariaSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Maquinaria.objects.all()

    def lastmod(self, obj):
        # Opcional: Si tuvieras un campo fecha_actualizacion, lo retornarías aquí.
        # Por ahora lo omitimos.
        return None
