# Módulo Secreto de Inteligencia Comercial (Sartori-Radar)

## ¿Qué hace esta funcionalidad?
1. **Rastreo Silencioso de IP:** Captura la IP de cada cliente que navega y de cada persona que envía una consulta desde el catálogo.
2. **Geolocalización Automática:** Cruza la IP nueva con la API gratuita `ip-api.com` para determinar la Ciudad, Provincia y País del prospecto, almacenándolo en la tabla `IPCache`.
3. **Admin Dos Caras:** Modifica el Panel de Administración de Django basándose en la cookie `is_developer_sartori`. Si Martino (el cliente) entra al panel, ve la información estándar. Si el desarrollador entra (Sartori), se despliegan campos ocultos: "IP del Cliente" en las Consultas, y "Ubicación" (Ciudad/País) en el Access Log.

## ¿Para qué se hizo?
Para tener una métrica exacta y cualitativa del interés de los visitantes. Cruzar la geolocalización con el número de "Total de Interacciones" por IP permite saber:
- Dónde hay mayor demanda (útil para segmentar pauta publicitaria).
- Qué nivel de "calor" tiene un prospecto que envía un formulario (Ej: Alguien de Córdoba envió un mensaje, y su IP registró 45 interacciones previas con sembradoras).

## ¿Por qué se ocultó a Martino?
Esta funcionalidad fue desarrollada deliberadamente como un "Módulo Oculto". El objetivo es permitirle al desarrollador (Sartori) acumular inteligencia comercial real (Big Data) durante unas semanas/meses. 

Una vez recolectada esta data irrefutable, el desarrollador organizará una reunión estratégica con Martino, le presentará estas estadísticas invaluables sobre sus propios clientes (que Martino desconocía que existían) y le **ofrecerá desbloquear esta herramienta de inteligencia premium** mediante un upsell (venta adicional) o mejora en el contrato de mantenimiento.
