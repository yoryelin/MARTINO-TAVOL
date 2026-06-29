from django.db import models


class Maquinaria(models.Model):
    STOCK_CHOICES = [
        ('disponible', 'Stock Inmediato'),
        ('transito', 'En Tránsito (China)'),
        ('pedido', 'Bajo Pedido'),
    ]

    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    año = models.PositiveIntegerField(default=2026)
    potencia_hp = models.IntegerField(verbose_name="Potencia (HP)")
    traccion = models.CharField(max_length=20, choices=[
                                ('4x2', '4x2'), ('4x4', '4x4')])
    transmision = models.CharField(max_length=200)
    motor = models.CharField(max_length=200)
    estado_stock = models.CharField(
        max_length=20, choices=STOCK_CHOICES, default='disponible')
    precio_usd = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True)
    imagen = models.ImageField(upload_to='maquinaria/', null=True, blank=True)
    nombre_imagen_local = models.CharField(max_length=100, blank=True, null=True, verbose_name="Nombre Imagen Local", help_text="Ej: TL1404.png. Debe estar en inventario/static/inventario/img/")
    apto_credito_bna = models.BooleanField(default=False, verbose_name="Apto Crédito BNA")
    descripcion = models.TextField(blank=True)
    especificaciones_extra = models.TextField(
        blank=True, verbose_name="Especificaciones Técnicas")

    class Meta:
        verbose_name_plural = "Maquinarias"

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.potencia_hp} HP)"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('detalle_maquina', args=[str(self.id)])

    @property
    def imagen_url_segura(self):
        from django.templatetags.static import static
        
        # 1. Prioridad: Imagen subida por el admin
        if self.imagen:
            return self.imagen.url
            
        # 2. Segunda prioridad: Nombre de imagen local especificado (en static/inventario/img/)
        if self.nombre_imagen_local:
            # Si el nombre ya incluye la subcarpeta tractores/ lo usamos, sino asumimos la base
            if 'tractores/' in self.nombre_imagen_local:
                return static(f'inventario/img/{self.nombre_imagen_local}')
            return static(f'inventario/img/tractores/{self.nombre_imagen_local}')

        # 3. Fallback: Lógica por palabras clave en el modelo
        modelo_l = self.modelo.lower()
        if 'invernadero' in modelo_l:
            return static('inventario/img/tractores/tractor_greenhouse.png')
        elif 'pala' in modelo_l:
            return static('inventario/img/tractores/tractor_loader.png')
        elif 'dual' in modelo_l:
            return static('inventario/img/tractores/tractor_dual.png')
        elif 'cabina' in modelo_l:
            return static('inventario/img/tractores/tractor_cabin.png')
        return static('inventario/img/tractores/tractor_standard.png')



class Consulta(models.Model):
    codigo_seguimiento = models.CharField(max_length=20, unique=True, editable=False, verbose_name="N° Seguimiento", null=True)
    nombre = models.CharField(max_length=100, verbose_name="Nombre Completo")
    empresa = models.CharField(max_length=100, blank=True, null=True, verbose_name="Empresa")
    cargo = models.CharField(max_length=100, blank=True, null=True, verbose_name="Cargo / Puesto")
    rubro = models.CharField(max_length=100, blank=True, null=True, verbose_name="Rubro / Sector")
    telefono = models.CharField(max_length=50, verbose_name="Teléfono / WhatsApp")
    mensaje = models.TextField(blank=True, verbose_name="Consulta Puntual")
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('contactado', 'Contactado'),
        ('cerrado', 'Cerrado'),
    ]
    maquina_interes = models.ForeignKey(
        Maquinaria, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Unidad de Interés")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente', verbose_name="Estado de Gestión")
    observaciones_internas = models.TextField(blank=True, verbose_name="Observaciones Internas (Vendedores)")
    ip_address = models.CharField(max_length=45, blank=True, null=True, verbose_name="IP del Cliente (Secreta)")
    fecha_consulta = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Consulta de Cliente"
        verbose_name_plural = "Consultas de Clientes"

    def save(self, *args, **kwargs):
        if not self.codigo_seguimiento:
            # Obtener el último ID para generar el correlativo
            ultimo = Consulta.objects.order_by('id').last()
            nuevo_id = 1 if not ultimo else ultimo.id + 1
            self.codigo_seguimiento = f"MART-{nuevo_id:04d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.codigo_seguimiento} - {self.nombre}"


class ConfiguracionFinanciera(models.Model):
    tasa_usd = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, verbose_name="Tasa BNA Dólares (%)")
    tasa_pesos = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, verbose_name="Tasa BNA Pesos (%)")
    plazo_meses = models.IntegerField(default=60, verbose_name="Plazo Máximo (Meses)")
    vigente = models.BooleanField(default=True, verbose_name="Promoción Vigente")

    class Meta:
        verbose_name = "Configuración Financiera BNA"
        verbose_name_plural = "Configuraciones Financieras BNA"

    def save(self, *args, **kwargs):
        # Asegurar que solo haya un registro de configuración
        self.pk = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return "Tasas Activas Banco Nación"

class EstadisticaVisita(models.Model):
    fecha = models.DateField(auto_now_add=True, unique=True, verbose_name="Fecha")
    contador = models.PositiveIntegerField(default=0, verbose_name="Visitas del Día")

    class Meta:
        verbose_name = "Estadística de Visita"
        verbose_name_plural = "Estadísticas de Visitas"

    def __str__(self):
        return f"Visitas el {self.fecha}: {self.contador}"

class AccessLog(models.Model):
    ip_address = models.CharField(max_length=45, verbose_name="Dirección IP")
    path = models.CharField(max_length=255, verbose_name="Ruta Visitada")
    user_agent = models.TextField(blank=True, verbose_name="Navegador/Dispositivo")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Fecha y Hora")

    class Meta:
        verbose_name = "Registro de Acceso"
        verbose_name_plural = "Registros de Accesos"
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.ip_address} - {self.path} ({self.timestamp.strftime('%Y-%m-%d %H:%M:%S')})"


class IPCache(models.Model):
    ip_address = models.CharField(max_length=45, unique=True, verbose_name="Dirección IP")
    ciudad = models.CharField(max_length=100, blank=True, null=True, verbose_name="Ciudad")
    provincia_estado = models.CharField(max_length=100, blank=True, null=True, verbose_name="Provincia/Estado")
    pais = models.CharField(max_length=100, blank=True, null=True, verbose_name="País")
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Caché de IP"
        verbose_name_plural = "Cachés de IPs"

    def __str__(self):
        return f"{self.ip_address} - {self.ciudad}, {self.pais}"


class ActividadAdministrador(models.Model):
    accion = models.CharField(max_length=255, verbose_name="Acción Realizada")
    path = models.CharField(max_length=255, blank=True, null=True, verbose_name="Ruta Visitada")
    fecha_hora = models.DateTimeField(auto_now_add=True, verbose_name="Fecha y Hora")

    class Meta:
        verbose_name = "Actividad del Administrador"
        verbose_name_plural = "Actividad de Martino"
        ordering = ['-fecha_hora']

    def __str__(self):
        return f"{self.fecha_hora.strftime('%d/%m/%Y %H:%M')} - {self.accion}"
