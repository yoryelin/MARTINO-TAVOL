from django.db.models import Sum
from django.utils import timezone
from inventario.models import Maquinaria, Consulta, ConfiguracionFinanciera, EstadisticaVisita

def admin_metrics(request):
    # Solo ejecutarse si estamos en el panel de administración
    if not (request.path.startswith('/admin/') or request.path.startswith('/sistema-martino/')):
        return {}
    
    if request.user.is_authenticated and request.user.is_staff:
        # Tasas BNA
        bna = ConfiguracionFinanciera.objects.first()
        
        # Métricas para el Operador (Inventario)
        total_maquinas = Maquinaria.objects.count()
        maquinas_disponibles = Maquinaria.objects.filter(estado_stock='disponible').count()
        maquinas_transito = Maquinaria.objects.filter(estado_stock='transito').count()
        maquinas_pedido = Maquinaria.objects.filter(estado_stock='pedido').count()
        
        # Métricas para el Vendedor (CRM / Ventas)
        total_consultas = Consulta.objects.count()
        consultas_pendientes = Consulta.objects.filter(estado='pendiente').count()
        consultas_contactadas = Consulta.objects.filter(estado='contactado').count()
        consultas_cerradas = Consulta.objects.filter(estado='cerrado').count()
        
        # Métricas de Visitas
        total_visitas = EstadisticaVisita.objects.aggregate(Sum('contador'))['contador__sum'] or 0
        hoy = timezone.now().date()
        visitas_hoy_obj = EstadisticaVisita.objects.filter(fecha=hoy).first()
        visitas_hoy = visitas_hoy_obj.contador if visitas_hoy_obj else 0

        # Consultas recientes para el Dashboard
        consultas_recientes = Consulta.objects.order_by('-fecha_consulta')[:5]
        
        return {
            'metrics': {
                'total_maquinas': total_maquinas,
                'maquinas_disponibles': maquinas_disponibles,
                'maquinas_transito': maquinas_transito,
                'maquinas_pedido': maquinas_pedido,
                'total_consultas': total_consultas,
                'consultas_pendientes': consultas_pendientes,
                'consultas_contactadas': consultas_contactadas,
                'consultas_cerradas': consultas_cerradas,
                'bna_usd': bna.tasa_usd if bna else 0,
                'bna_pesos': bna.tasa_pesos if bna else 0,
                'bna_vigente': bna.vigente if bna else False,
                'total_visitas': total_visitas,
                'visitas_hoy': visitas_hoy,
            },
            'consultas_recientes': consultas_recientes
        }
    return {}
