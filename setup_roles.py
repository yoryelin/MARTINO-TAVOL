import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agro_import.settings')
django.setup()

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from inventario.models import Maquinaria, Consulta, ConfiguracionFinanciera

def setup_roles():
    print("Iniciando la configuración de Roles y Permisos (RBAC)...")

    # 1. Crear los grupos
    grupo_admin, created = Group.objects.get_or_create(name='Administrador Jefe')
    if created:
        print("Grupo 'Administrador Jefe' creado.")
    
    grupo_operador, created = Group.objects.get_or_create(name='Operador')
    if created:
        print("Grupo 'Operador' creado.")

    grupo_vendedor, created = Group.objects.get_or_create(name='Vendedor')
    if created:
        print("Grupo 'Vendedor' creado.")

    # 2. Obtener los ContentTypes para nuestros modelos
    ct_maquinaria = ContentType.objects.get_for_model(Maquinaria)
    ct_consulta = ContentType.objects.get_for_model(Consulta)
    ct_config = ContentType.objects.get_for_model(ConfiguracionFinanciera)

    # Permisos para Maquinaria
    perm_view_maq = Permission.objects.get(content_type=ct_maquinaria, codename='view_maquinaria')
    perm_add_maq = Permission.objects.get(content_type=ct_maquinaria, codename='add_maquinaria')
    perm_change_maq = Permission.objects.get(content_type=ct_maquinaria, codename='change_maquinaria')
    
    # Permisos para Consulta
    perm_view_cons = Permission.objects.get(content_type=ct_consulta, codename='view_consulta')
    perm_change_cons = Permission.objects.get(content_type=ct_consulta, codename='change_consulta')
    
    # Permisos para Configuracion Financiera
    perm_view_config = Permission.objects.get(content_type=ct_config, codename='view_configuracionfinanciera')

    # 3. Asignar permisos al Administrador Jefe
    # El administrador jefe recibe absolutamente TODOS los permisos de la base de datos
    todos_los_permisos = Permission.objects.all()
    grupo_admin.permissions.set(todos_los_permisos)
    print("Permisos Totales asignados al grupo 'Administrador Jefe'.")

    # 4. Asignar permisos al Operador
    # Operador puede: Ver, Añadir, Cambiar (pero NO eliminar) Maquinaria.
    # Operador puede: Ver Consultas (pero NO borrarlas ni editarlas).
    grupo_operador.permissions.set([
        perm_view_maq, perm_add_maq, perm_change_maq,
        perm_view_cons
    ])
    print("Permisos asignados al grupo 'Operador'.")

    # 5. Asignar permisos al Vendedor
    # Vendedor puede: Ver Maquinaria (NO añadir, NO cambiar, NO eliminar) -> Así NO puede alterar el esquema de precios.
    # Vendedor puede: Ver y Cambiar Consultas (Para seguimiento de clientes).
    # Vendedor puede: Ver ConfiguracionFinanciera (Para poder ver las tasas BNA, pero NO modificarlas).
    grupo_vendedor.permissions.set([
        perm_view_maq,
        perm_view_cons, perm_change_cons,
        perm_view_config
    ])
    print("Permisos asignados al grupo 'Vendedor'.")

    print("\n¡Configuración de roles completada con éxito!")

if __name__ == '__main__':
    setup_roles()
