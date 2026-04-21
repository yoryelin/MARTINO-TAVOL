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
    descripcion = models.TextField(blank=True)
    especificaciones_extra = models.TextField(
        blank=True, verbose_name="Especificaciones Técnicas")

    class Meta:
        verbose_name_plural = "Maquinarias"

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.potencia_hp} HP)"


class Consulta(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=50)
    mensaje = models.TextField(blank=True)
    maquina_interes = models.ForeignKey(
        Maquinaria, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Unidad de Interés")
    fecha_consulta = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Consulta de Cliente"
        verbose_name_plural = "Consultas de Clientes"

    def __str__(self):
        return f"Consulta de {self.nombre} - {self.fecha_consulta.strftime('%d/%m/%Y')}"
