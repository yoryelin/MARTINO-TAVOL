from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Maquinaria, Consulta


def home(request):
    featured = Maquinaria.objects.all()[:3]
    return render(request, 'inventario/landing.html', {'featured': featured})


def catalogo(request):
    maquinas = Maquinaria.objects.all()
    return render(request, 'inventario/catalogo.html', {'maquinas': maquinas})


def detalle_maquina(request, pk):
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
    
    context = {
        'm': maquina,
        'specs': specs_list,
        'relacionados': relacionados
    }
    return render(request, 'inventario/detalle_maquina.html', context)


@require_POST
def enviar_consulta(request):
    nombre = request.POST.get('nombre')
    telefono = request.POST.get('telefono')
    mensaje = request.POST.get('mensaje')
    maquina_nombre = request.POST.get('maquina_nombre')

    maquina = None
    if maquina_nombre:
        maquina = Maquinaria.objects.filter(modelo=maquina_nombre).first()

    # Guardar en base de datos
    consulta = Consulta.objects.create(
        nombre=nombre,
        telefono=telefono,
        mensaje=mensaje,
        maquina_interes=maquina
    )

    return JsonResponse({'status': 'success', 'id': consulta.id})
# Create your views here.
