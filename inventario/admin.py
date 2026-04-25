from django.contrib import admin
from django.utils.safestring import mark_safe
from django.templatetags.static import static
from .models import Maquinaria, Consulta

@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ('codigo_seguimiento', 'nombre', 'empresa', 'rubro', 'telefono', 'fecha_consulta')
    list_filter = ('rubro', 'maquina_interes', 'fecha_consulta')
    search_fields = ('codigo_seguimiento', 'nombre', 'empresa', 'telefono')
    readonly_fields = ('codigo_seguimiento', 'fecha_consulta')
    date_hierarchy = 'fecha_consulta'
    ordering = ('-fecha_consulta',)

@admin.register(Maquinaria)
class MaquinariaAdmin(admin.ModelAdmin):
    list_display = ('thumbnail', 'marca', 'modelo', 'potencia_hp', 'estado_stock')
    list_filter = ('marca', 'estado_stock', 'traccion')
    search_fields = ('marca', 'modelo', 'descripcion')
    readonly_fields = ('preview_imagen',)
    
    fieldsets = (
        ('Identidad de Unidad', {
            'fields': ('marca', 'modelo', 'año', 'estado_stock')
        }),
        ('Especificaciones Técnicas', {
            'fields': (('potencia_hp', 'traccion'), ('motor', 'transmision'), 'especificaciones_extra')
        }),
        ('Contenido Visual y Comercial', {
            'fields': ('imagen', 'nombre_imagen_local', 'preview_imagen', 'descripcion', 'precio_usd'),
            'description': 'Aquí puedes subir la foto real o dejar que el sistema asigne una por defecto según el modelo.'
        }),
    )

    def thumbnail(self, obj):
        url = self._get_smart_image_url(obj)
        return mark_safe(f'<img src="{url}" width="60" style="border-radius: 5px; border: 1px solid #ddd; display: block;" />')
    thumbnail.short_description = "Vista"

    def preview_imagen(self, obj):
        if not obj.pk: return ""
        url = self._get_smart_image_url(obj)
        return mark_safe(f'<div><img src="{url}" width="350" style="border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.2); border: 2px solid #eee;" /><p style="margin-top:10px; color:#666; font-style: italic;">Previsualización actual del equipo</p></div>')
    preview_imagen.short_description = "Vista Previa"

    def _get_smart_image_url(self, obj):
        # 1. Imagen local estática vinculada manualmente (Opción A)
        if getattr(obj, 'nombre_imagen_local', None):
            return static(f'inventario/img/{obj.nombre_imagen_local}')
            
        # 2. Lógica de imagen subida desde el Admin
        if obj.imagen:
            return obj.imagen.url
        
        # Fallback a imágenes estáticas según categoría
        modelo_l = obj.modelo.lower()
        if 'invernadero' in modelo_l:
            return static('inventario/img/tractores/tractor_greenhouse.png')
        elif 'pala' in modelo_l:
            return static('inventario/img/tractores/tractor_loader.png')
        elif 'dual' in modelo_l:
            return static('inventario/img/tractores/tractor_dual.png')
        elif 'cabina' in modelo_l:
            return static('inventario/img/tractores/tractor_cabin.png')
        return static('inventario/img/tractores/tractor_standard.png')

