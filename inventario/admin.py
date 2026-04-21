from django.contrib import admin
from .models import Maquinaria, Consulta


@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono', 'maquina_interes', 'fecha_consulta')
    list_filter = ('maquina_interes', 'fecha_consulta')
    search_fields = ('nombre', 'telefono', 'mensaje')
    readonly_fields = ('fecha_consulta',)
    date_hierarchy = 'fecha_consulta'
    ordering = ('-fecha_consulta',)


@admin.register(Maquinaria)
class MaquinariaAdmin(admin.ModelAdmin):
    list_display = ('marca', 'modelo', 'potencia_hp', 'estado_stock', 'tiene_imagen')
    list_filter = ('marca', 'estado_stock')
    search_fields = ('modelo', 'descripcion')
    readonly_fields = ('tiene_imagen',)

    fieldsets = (
        ('Información General', {
            'fields': ('marca', 'modelo', 'año', 'estado_stock', 'precio_usd')
        }),
        ('Especificaciones Técnicas', {
            'fields': ('potencia_hp', 'traccion', 'transmision', 'motor', 'especificaciones_extra')
        }),
        ('Contenido Visual', {
            'fields': ('imagen', 'descripcion')
        }),
    )

    def tiene_imagen(self, obj):
        return bool(obj.imagen)
    tiene_imagen.boolean = True
    tiene_imagen.short_description = "Imagen"
