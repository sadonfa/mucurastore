from django.core.validators import MaxValueValidator
from django.db import models
from customers.models import Customers
from products.models import Products

# Create your models here.

# Opciones de pago
PAGO_CHOICES = [
    ('efectivo', 'Efectivo'),
    ('cxc', 'Cuenta por Cobrar'),
    ('transferencia', 'Transferencia Bancaria'),
    ('otro', 'Otro'),
]

class Orders(models.Model):
    cliente = models.ForeignKey(Customers, on_delete=models.CASCADE, verbose_name="Cliente")
    name = models.CharField(max_length=150, verbose_name="Nombre")
    description = models.CharField(max_length=250, verbose_name="Descripcion")
    created = models.DateTimeField(auto_now_add=True, verbose_name='Creacion' )
    updated = models.DateTimeField(auto_now=True, verbose_name='Actualizacion' )
     # NUEVO CAMPO PARA LA FORMA DE PAGO
    forma_pago = models.CharField(
        max_length=50,
        choices=PAGO_CHOICES,
        default='efectivo',
        verbose_name="Forma de Pago"
    )

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

    def __str__(self):
        return self.name

class Article(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, verbose_name="Pedido")
    product = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name="Producto")
    cantidad = models.IntegerField(default=0, verbose_name="Cantidad")
    cash= models.DecimalField(max_digits=10, decimal_places=2, validators=[MaxValueValidator(9999.99)])
    created = models.DateField(auto_now_add=True, verbose_name='Creacion' )
    updated = models.DateField(auto_now=True, verbose_name='Actualizacion' )

    class Meta:
        verbose_name = "Articulo"
        verbose_name_plural = "Articulos"

    def __str__(self):
        return self.name
