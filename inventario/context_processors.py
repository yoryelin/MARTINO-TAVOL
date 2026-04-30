from inventario.models import Maquinaria, Consulta

def admin_metrics(request):
    # Solo ejecutarse si estamos en el panel de administración
    if not request.path.startswith('/admin/'):
        return {}
    
    if request.user.is_authenticated and request.user.is_staff:
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
            },
            'consultas_recientes': consultas_recientes
        }
    return {}
