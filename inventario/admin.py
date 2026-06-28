from django.contrib import admin
from django.utils.safestring import mark_safe
from django.templatetags.static import static
from .models import Maquinaria, Consulta, ConfiguracionFinanciera, AccessLog

@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ('codigo_seguimiento', 'nombre', 'estado', 'empresa', 'rubro', 'telefono', 'fecha_consulta')
    list_filter = ('estado', 'rubro', 'maquina_interes', 'fecha_consulta')
    search_fields = ('codigo_seguimiento', 'nombre', 'empresa', 'telefono', 'observaciones_internas')
    readonly_fields = ('codigo_seguimiento', 'fecha_consulta')
    date_hierarchy = 'fecha_consulta'
    ordering = ('-fecha_consulta',)

@admin.register(Maquinaria)
class MaquinariaAdmin(admin.ModelAdmin):
    list_display = ('thumbnail', 'marca', 'modelo', 'potencia_hp', 'estado_stock', 'apto_credito_bna')
    list_filter = ('marca', 'estado_stock', 'traccion', 'apto_credito_bna')
    search_fields = ('marca', 'modelo', 'descripcion')
    readonly_fields = ('preview_imagen',)
    
    fieldsets = (
        ('Información Principal', {
            'fields': ('marca', 'modelo', 'año', 'potencia_hp', 'precio_usd', 'apto_credito_bna')
        }),
        ('Especificaciones Técnicas', {
            'fields': ('traccion', 'transmision', 'motor', 'descripcion', 'especificaciones_extra')
        }),
        ('Imágenes y Stock', {
            'fields': ('estado_stock', 'imagen', 'nombre_imagen_local', 'preview_imagen')
        }),
    )

    def get_imagen_url(self, obj):
        return obj.imagen_url_segura

    def thumbnail(self, obj):
        url = self.get_imagen_url(obj)
        if url:
            return mark_safe(f'<img src="{url}" width="50" height="50" style="object-fit: contain; border-radius: 5px; background: #fff; padding: 2px;" />')
        return "Sin imagen"
    thumbnail.short_description = 'Imagen'

    def preview_imagen(self, obj):
        url = self.get_imagen_url(obj)
        if url:
            return mark_safe(f'<img src="{url}" width="300" style="object-fit: contain; border-radius: 10px; background: #f8f9fa; padding: 10px; border: 1px solid #dee2e6;" />')
        return "Guarde el modelo para ver la imagen generada automáticamente"
    preview_imagen.short_description = 'Vista Previa'

@admin.register(ConfiguracionFinanciera)
class ConfiguracionFinancieraAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'tasa_usd', 'tasa_pesos', 'plazo_meses', 'vigente')
    
    def has_add_permission(self, request):
        # Solo permitir un registro de configuración
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

@admin.register(AccessLog)
class AccessLogAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'path', 'timestamp', 'user_agent')
    list_filter = ('timestamp', 'ip_address')
    search_fields = ('ip_address', 'path', 'user_agent')
    readonly_fields = ('ip_address', 'path', 'user_agent', 'timestamp')

    def has_module_permission(self, request):
        return request.COOKIES.get('is_developer_sartori') == 'true'

    def has_view_permission(self, request, obj=None):
        return request.COOKIES.get('is_developer_sartori') == 'true'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.COOKIES.get('is_developer_sartori') == 'true'
