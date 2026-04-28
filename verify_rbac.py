import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agro_import.settings')
django.setup()

from django.contrib.auth.models import User, Group

def run_simulation():
    print("=== INICIANDO SIMULACIÓN VIRTUAL DE PERMISOS (RBAC) ===")
    
    # Asegurarnos de que el grupo Vendedor existe
    try:
        grupo_vendedor = Group.objects.get(name='Vendedor')
    except Group.DoesNotExist:
        print("❌ ERROR: El grupo 'Vendedor' no existe. ¿Ejecutaste setup_roles.py?")
        return

    # Crear un usuario virtual temporal para la simulación
    user_sim, created = User.objects.get_or_create(username='simulacion_vendedor')
    user_sim.groups.add(grupo_vendedor)
    
    print("\nVerificando los permisos del usuario 'simulacion_vendedor' asignado al grupo Vendedor...\n")

    # Pruebas sobre Maquinaria (Inventario)
    print("--- MÓDULO: MAQUINARIA (TRACTORES) ---")
    print(f"¿Puede VER tractores?         {'✅ SÍ' if user_sim.has_perm('inventario.view_maquinaria') else '❌ NO'}")
    print(f"¿Puede AÑADIR tractores?      {'✅ SÍ' if user_sim.has_perm('inventario.add_maquinaria') else '❌ NO (Bloqueado)'}")
    print(f"¿Puede CAMBIAR tractores?     {'✅ SÍ' if user_sim.has_perm('inventario.change_maquinaria') else '❌ NO (Bloqueado)'}")
    print(f"¿Puede ELIMINAR tractores?    {'✅ SÍ' if user_sim.has_perm('inventario.delete_maquinaria') else '❌ NO (Bloqueado)'}")

    # Pruebas sobre Configuración Financiera (BNA)
    print("\n--- MÓDULO: CONFIGURACIÓN FINANCIERA (BNA) ---")
    print(f"¿Puede VER tasas BNA?         {'✅ SÍ' if user_sim.has_perm('inventario.view_configuracionfinanciera') else '❌ NO'}")
    print(f"¿Puede CAMBIAR tasas BNA?     {'✅ SÍ' if user_sim.has_perm('inventario.change_configuracionfinanciera') else '❌ NO (Bloqueado)'}")

    # Pruebas sobre Consultas
    print("\n--- MÓDULO: CONSULTAS DE CLIENTES ---")
    print(f"¿Puede VER consultas?         {'✅ SÍ' if user_sim.has_perm('inventario.view_consulta') else '❌ NO'}")
    print(f"¿Puede CAMBIAR estado/notas?  {'✅ SÍ' if user_sim.has_perm('inventario.change_consulta') else '❌ NO'}")
    print(f"¿Puede ELIMINAR consultas?    {'✅ SÍ' if user_sim.has_perm('inventario.delete_consulta') else '❌ NO (Bloqueado)'}")

    # Pruebas sobre Usuarios
    print("\n--- MÓDULO: USUARIOS ---")
    print(f"¿Puede ADMINISTRAR usuarios?  {'✅ SÍ' if user_sim.has_perm('auth.view_user') or user_sim.has_perm('auth.add_user') else '❌ NO (Bloqueado)'}")

    # Limpiar el usuario virtual
    user_sim.delete()
    print("\n=== SIMULACIÓN FINALIZADA Y LIMPIADA ===")

if __name__ == '__main__':
    run_simulation()
