import os
import django

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agro_import.settings')
django.setup()

from inventario.models import Maquinaria

def seed_data():
    print("Iniciando carga de catálogo MARTINO - TAVOL...")
    
    # Limpiar datos existentes si se desea (opcional, aquí lo mantengo para no borrar lo que el usuario cargó)
    # Maquinaria.objects.all().delete()

    tractores = [
        # SERIE INVERNADERO
        {
            'marca': 'TAVOL',
            'modelo': 'TL304 Invernadero',
            'potencia_hp': 30,
            'traccion': '4x4',
            'transmision': '8F+2R (Engranaje deslizante)',
            'motor': 'Diesel 4 cilindros Euro II',
            'descripcion': 'Diseñado específicamente para invernáculos y jardines. Estructura compacta con pequeño radio de giro para maniobrar en hileras estrechas. Ideal para espacios confinados.',
            'especificaciones_extra': 'Dirección hidráulica, embrague simple, Neumáticos especiales para invernadero. Implementos compatibles: arado de disco, rastra, rotocultivador.',
            'estado_stock': 'disponible'
        },
        {
            'marca': 'TAVOL',
            'modelo': 'TL504 Invernadero',
            'potencia_hp': 50,
            'traccion': '4x4',
            'transmision': '8F+2R con inversor',
            'motor': 'YTO 4 cilindros de alta eficiencia',
            'descripcion': 'Serie Greenhouse-King. Compacto para espacios reducidos sin sacrificar capacidad de carga y tracción. Versatilidad total para cultivos protegidos.',
            'especificaciones_extra': '2 grupos de salida hidráulica, PTO 540/760 rpm, levante de 3 puntos categoría I.',
            'estado_stock': 'transito'
        },
        {
            'marca': 'TAVOL',
            'modelo': 'TL704 Invernadero',
            'potencia_hp': 70,
            'traccion': '4x4',
            'transmision': '8F+8R Sincronizada',
            'motor': '4 cilindros Inyección Directa',
            'descripcion': 'La máxima potencia en formato compacto. Adaptado para invernaderos de gran escala. Combina fuerza de tiro con dimensiones reducidas.',
            'especificaciones_extra': 'Peso aproximado 1.980 kg. Neumáticos especiales para suelo húmedo. PTO de dos velocidades.',
            'estado_stock': 'pedido'
        },
        
        # TRACTORES ESTÁNDAR
        {
            'marca': 'TAVOL',
            'modelo': 'TL504',
            'potencia_hp': 50,
            'traccion': '4x4',
            'transmision': '8F+2R',
            'motor': 'Quanchai/YTO 4 cilindros',
            'descripcion': 'Tractor utilitario versátil para tareas generales de campo. Equilibrio perfecto entre consumo y productividad.',
            'especificaciones_extra': 'Depósito de 60L, Capacidad de levante 1.000 kg, PTO 540/760 rpm. Dimensiones: 3300x1440x2450 mm.',
            'estado_stock': 'disponible'
        },
        {
            'marca': 'TAVOL',
            'modelo': 'TL504 con Cabina',
            'potencia_hp': 50,
            'traccion': '4x4',
            'transmision': '8F+2R con Inversor',
            'motor': '4 cilindros Refrigerado por Agua',
            'descripcion': 'Versión confort del TL504. Cabina cerrada con aire acondicionado y calefacción. Ideal para jornadas prolongadas bajo el sol.',
            'especificaciones_extra': 'Cabina panorámica, Asiento con suspensión, Radio, Aire Acondicionado, 2 grupos hidráulicos.',
            'estado_stock': 'disponible'
        },
        {
            'marca': 'TAVOL',
            'modelo': 'TL704',
            'potencia_hp': 70,
            'traccion': '4x4',
            'transmision': '8F+8R Sincronizada',
            'motor': 'Yangdong/Weichai Stage II',
            'descripcion': 'Tractor de potencia media para labranza y transporte. Robusto y confiable con bajos costos de mantenimiento.',
            'especificaciones_extra': 'Embrague doble etapa, Freno de disco húmedo, Neumáticos 7.5-20 / 12.4-28. Certificación CE.',
            'estado_stock': 'transito'
        },
        {
            'marca': 'TAVOL',
            'modelo': 'TL704 con Cabina',
            'potencia_hp': 70,
            'traccion': '4x4',
            'transmision': '12F+12R (Opcional)',
            'motor': '4 cilindros Inyección Directa',
            'descripcion': 'Tractor de 70 HP con cabina climatizada de alto confort. Excelente visibilidad y aislamiento acústico.',
            'especificaciones_extra': 'Espejo retrovisor interno, cinturón de seguridad, Aire Acondicionado, Luces LED de trabajo.',
            'estado_stock': 'disponible'
        },

        # MEDIA - ALTA POTENCIA
        {
            'marca': 'TAVOL',
            'modelo': 'TL904 con Cabina',
            'potencia_hp': 90,
            'traccion': '4x4',
            'transmision': '12F+12R con Inversor',
            'motor': '4 cilindros 4.087 cc / 66,2 kW',
            'descripcion': 'Potencia para tareas exigentes. Chasis reforzado y sistema hidráulico de alto flujo.',
            'especificaciones_extra': 'Embrague doble disco seco, Hidráulica separada con capacidad de 1.820 kg. Contrapesos delanteros y traseros incluidos.',
            'estado_stock': 'pedido'
        },
        {
            'marca': 'TAVOL',
            'modelo': 'TL1004 con Cabina',
            'potencia_hp': 100,
            'traccion': '4x4',
            'transmision': '12F+12R',
            'motor': 'Turbo Diesel 4 cilindros',
            'descripcion': 'El estándar de los 100 HP. Diseñado para subsolado y siembra de precisión. Gran estabilidad en terrenos irregulares.',
            'especificaciones_extra': 'Peso 3.000 kg. PTO 540/760/1000 rpm. Certificado ISO y CE.',
            'estado_stock': 'disponible'
        },
        {
            'marca': 'TAVOL',
            'modelo': 'TL1404 con Cabina',
            'potencia_hp': 140,
            'traccion': '4x4',
            'transmision': '16F+8R High-Range',
            'motor': '6 cilindros Turbo Intercooler',
            'descripcion': 'Alta potencia para grandes extensiones. Capacidad para trabajar con implementos de gran ancho de labor.',
            'especificaciones_extra': 'Apto para subsolado profundo y siembra pesada. Certificaciones Internacionales EPA/CE.',
            'estado_stock': 'pedido'
        },
        {
            'marca': 'TAVOL',
            'modelo': 'TL1804 con Cabina y Duales',
            'potencia_hp': 180,
            'traccion': '4x4',
            'transmision': '16F+16R Sincronizada',
            'motor': '6 cilindros Heavy Duty',
            'descripcion': 'El buque insignia de la línea. Tracción máxima con ruedas duales traseras para minimizar la compactación del suelo.',
            'especificaciones_extra': 'Configuración de duales incluida, Cabina Premium AC, Máximo flujo hidráulico para sembradoras neumáticas.',
            'estado_stock': 'pedido'
        },

        # CON PALA FRONTAL
        {
            'marca': 'TAVOL',
            'modelo': 'TL704 con Cabina y Pala Frontal',
            'potencia_hp': 70,
            'traccion': '4x4',
            'transmision': '8F+8R con inversor',
            'motor': '4 cilindros Torque Alto',
            'descripcion': 'Equipo multifunción. Combina la potencia de un tractor de 70 HP con la versatilidad de una cargadora frontal.',
            'especificaciones_extra': 'Pala cargadora hidráulica reforzada, Joystick de control en cabina, Enganche de 3 puntos trasero funcional.',
            'estado_stock': 'transito'
        },
        {
            'marca': 'TAVOL',
            'modelo': 'TL1004 con Cabina y Pala Frontal',
            'potencia_hp': 100,
            'traccion': '4x4',
            'transmision': '12F+12R',
            'motor': 'Turbo Diesel 100 HP',
            'descripcion': 'Máxima capacidad de carga y movimiento de suelos. La herramienta definitiva para el feedlot o mantenimiento de caminos.',
            'especificaciones_extra': 'Pala frontal de gran capacidad, Cabina AC, Peso operativo con pala 3.800 kg aproximadamente.',
            'estado_stock': 'pedido'
        }
    ]

    for data in tractores:
        obj, created = Maquinaria.objects.get_or_create(
            marca=data['marca'],
            modelo=data['modelo'],
            defaults=data
        )
        if created:
            print(f"  + Agregado: {data['modelo']}")
        else:
            # Actualizar datos si ya existe para asegurar que tenga la nueva info de la IA
            for key, value in data.items():
                setattr(obj, key, value)
            obj.save()
            print(f"  * Actualizado: {data['modelo']}")

    print("\n¡Carga completada con éxito! Ya puedes ver el catálogo en el sitio.")

if __name__ == '__main__':
    seed_data()
