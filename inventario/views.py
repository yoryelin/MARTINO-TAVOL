from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import Maquinaria, Consulta, ConfiguracionFinanciera, EstadisticaVisita

def registrar_visita():
    # Helper para incrementar el contador diario
    hoy = timezone.now().date()
    # Usamos get_or_create para crear el registro del día si no existe
    stat, created = EstadisticaVisita.objects.get_or_create(fecha=hoy)
    stat.contador += 1
    stat.save()


def home(request):
    registrar_visita()
    featured = Maquinaria.objects.all()[:3]
    return render(request, 'inventario/landing.html', {'featured': featured})


def catalogo(request):
    registrar_visita()
    maquinas = Maquinaria.objects.all()
    return render(request, 'inventario/catalogo.html', {'maquinas': maquinas})


def detalle_maquina(request, pk):
    registrar_visita()
    maquina = get_object_or_404(Maquinaria, pk=pk)
    
    # Procesar especificaciones_extra (Clave: Valor) para la tabla
    specs_list = []
    if maquina.especificaciones_extra:
        lines = maquina.especificaciones_extra.split('\n')
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                specs_list.append({'key': key.strip(), 'value': value.strip()})
    
    # Sugerir otras 3 unidades (excluyendo la actual)
    relacionados = Maquinaria.objects.exclude(pk=pk)[:3]
    # Configuracion Financiera (Si la máquina es apta crédito)
    financiacion = None
    if maquina.apto_credito_bna:
        financiacion = ConfiguracionFinanciera.objects.first()
        # Si no existe configuración en la BD, no enviamos nada al contexto
        # para que el cliente sea el único responsable de activarlo.
    
    context = {
        'm': maquina,
        'specs': specs_list,
        'relacionados': relacionados,
        'financiacion': financiacion
    }
    return render(request, 'inventario/detalle_maquina.html', context)


@require_POST
def enviar_consulta(request):
    nombre = request.POST.get('nombre')
    empresa = request.POST.get('empresa')
    cargo = request.POST.get('cargo')
    rubro = request.POST.get('rubro')
    telefono = request.POST.get('telefono')
    mensaje = request.POST.get('mensaje')
    maquina_nombre = request.POST.get('maquina_nombre')

    maquina = None
    if maquina_nombre:
        maquina = Maquinaria.objects.filter(modelo=maquina_nombre).first()

    # Obtener IP secreta
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    # Guardar en base de datos
    consulta = Consulta.objects.create(
        nombre=nombre,
        empresa=empresa,
        cargo=cargo,
        rubro=rubro,
        telefono=telefono,
        mensaje=mensaje,
        maquina_interes=maquina,
        ip_address=ip
    )

    return JsonResponse({'status': 'success', 'id': consulta.id})

from django.http import HttpResponse

def activar_radar_maquinaria(request):
    response = HttpResponse("Radar activado exitosamente. Modo fantasma ON.")
    # Instalamos la cookie invisible por 10 años
    response.set_cookie('is_developer_sartori', 'true', max_age=315360000)
    return response
