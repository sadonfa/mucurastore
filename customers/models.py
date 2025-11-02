from django.db import models

# Create your models here.

class Customers(models.Model):
    name = models.CharField(max_length=150, verbose_name="Nombre")
    lastname = models.CharField(max_length=150, verbose_name="Apellidos")
    email = models.EmailField(verbose_name="Correo")
    movil = models.CharField(max_length=150, verbose_name="Telefono")
    created = models.DateField(auto_now_add=True, verbose_name='Creacion' )
    updated = models.DateField(auto_now=True, verbose_name='Actualizacion' )

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return self.name
