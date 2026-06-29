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

    def get_list_display(self, request):
        if request.COOKIES.get('is_developer_sartori') == 'true':
            return ('codigo_seguimiento', 'nombre', 'estado', 'empresa', 'rubro', 'telefono', 'ip_address', 'fecha_consulta')
        return ('codigo_seguimiento', 'nombre', 'estado', 'empresa', 'rubro', 'telefono', 'fecha_consulta')

    def get_readonly_fields(self, request, obj=None):
        if request.COOKIES.get('is_developer_sartori') == 'true':
            return ('codigo_seguimiento', 'fecha_consulta', 'ip_address')
        return ('codigo_seguimiento', 'fecha_consulta')

    def get_fields(self, request, obj=None):
        # Campos por defecto para Martino
        fields = ['codigo_seguimiento', 'nombre', 'empresa', 'cargo', 'rubro', 'telefono', 'mensaje', 'maquina_interes', 'estado', 'observaciones_internas', 'fecha_consulta']
        if request.COOKIES.get('is_developer_sartori') == 'true':
            fields.insert(len(fields)-1, 'ip_address')
        return fields

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
    list_display = ('ip_address', 'ubicacion', 'visitas_totales', 'path', 'timestamp')
    list_filter = ('timestamp', 'ip_address')
    search_fields = ('ip_address', 'path', 'user_agent')
    readonly_fields = ('ip_address', 'path', 'user_agent', 'timestamp')

    def ubicacion(self, obj):
        from .models import IPCache
        cache = IPCache.objects.filter(ip_address=obj.ip_address).first()
        if cache and cache.ciudad:
            return f"{cache.ciudad}, {cache.provincia_estado} ({cache.pais})"
        return "Desconocida / Analizando..."
    ubicacion.short_description = "Ciudad/País"

    def changelist_view(self, request, extra_context=None):
        if request.COOKIES.get('is_developer_sartori') == 'true':
            from .models import AccessLog, IPCache
            # Contar interacciones por IP
            stats = {}
            for log in AccessLog.objects.all():
                if log.ip_address not in stats:
                    stats[log.ip_address] = 0
                stats[log.ip_address] += 1
            
            # Agrupar por ciudad/ubicación
            ubicaciones = {}
            for ip, count in stats.items():
                cache = IPCache.objects.filter(ip_address=ip).first()
                if cache and cache.ciudad:
                    loc = f"{cache.ciudad}, {cache.provincia_estado} ({cache.pais})"
                else:
                    loc = "Desconocida / Pendiente"
                
                if loc not in ubicaciones:
                    ubicaciones[loc] = 0
                ubicaciones[loc] += count
            
            # Ordenar de mayor a menor y agarrar el top
            top_ubicaciones = sorted(ubicaciones.items(), key=lambda x: x[1], reverse=True)
            
            extra_context = extra_context or {}
            extra_context['top_ubicaciones'] = top_ubicaciones
            
        return super().changelist_view(request, extra_context=extra_context)

    def visitas_totales(self, obj):
        # Cuenta cuántas veces aparece esta IP en toda la tabla
        return AccessLog.objects.filter(ip_address=obj.ip_address).count()
    visitas_totales.short_description = 'Total Interacciones'

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
