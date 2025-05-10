from django.db import models
from django.utils import timezone 
class TipoDocumento(models.Model):
    nombre_tipo = models.CharField(max_length=100, unique=True, verbose_name="Nombre del Tipo de Documento")
    abreviatura = models.CharField(max_length=10, unique=True, verbose_name="Abreviatura")

    def __str__(self):
        return self.nombre_tipo

    class Meta:
        verbose_name = "Tipo de Documento"
        verbose_name_plural = "Tipos de Documento"

class Cliente(models.Model):
    tipo_documento = models.ForeignKey(TipoDocumento, on_delete=models.PROTECT, verbose_name="Tipo de Documento")
    numero_documento = models.CharField(max_length=50, unique=True, verbose_name="Número de Documento")
    nombre = models.CharField(max_length=100, verbose_name="Nombres")
    apellido = models.CharField(max_length=100, verbose_name="Apellidos")
    correo = models.EmailField(max_length=254, unique=True, verbose_name="Correo Electrónico")
    telefono = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono")
    fecha_registro = models.DateTimeField(default=timezone.now, verbose_name="Fecha de Registro")


    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.numero_documento})"

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['apellido', 'nombre']

class Compra(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="compras", verbose_name="Cliente")
    fecha_compra = models.DateTimeField(verbose_name="Fecha de Compra")
    monto_compra = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Monto de la Compra (COP)")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción de la Compra")


    def __str__(self):
        return f"Compra de {self.cliente} por {self.monto_compra} el {self.fecha_compra.strftime('%Y-%m-%d')}"

    class Meta:
        verbose_name = "Compra"
        verbose_name_plural = "Compras"
        ordering = ['-fecha_compra']