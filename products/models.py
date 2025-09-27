from django.db import models
from django.core.validators import MaxValueValidator

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name="Nombre")
    description = models.CharField(max_length=250, verbose_name="Descripcion")
    created = models.DateField(auto_now_add=True, verbose_name='Creacion' )
    updated = models.DateField(auto_now=True, verbose_name='Actualizacion' )

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.name

class Products(models.Model):
    name = models.CharField(max_length=150, verbose_name="Nombre")
    description = models.CharField(max_length=150, verbose_name="Descripcion")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    stock = models.IntegerField(default=0, verbose_name="Stock")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True, verbose_name='Creacion' )
    updated = models.DateField(auto_now=True, verbose_name='Actualizacion' )

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return self.name


