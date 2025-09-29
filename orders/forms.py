from django import forms
from django.forms import inlineformset_factory
from .models import Orders, Article, Products

# 1. Formulario principal para el encabezado del Pedido
class OrderForm(forms.ModelForm):
    class Meta:
        model = Orders
        # Solo necesitamos el cliente, el nombre y la descripción para el encabezado.
        fields = ['cliente', 'forma_pago']
        labels = {
            'cliente': 'Cliente',
        }

# 2. Formulario para cada línea de Artículo (Article)
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        # El campo 'order' se llena automáticamente por el formset, 
        # así que solo necesitamos producto, cantidad y cash.
        fields = ['product', 'cantidad', 'cash']

        # Bloquear el campo 'cash' usando widgets
        widgets = {
            'cash': forms.TextInput(attrs={'readonly': 'readonly'}),
        }
        

        labels = {
            'product': 'Producto',
            'cantidad': 'Cantidad',
            'cash': 'Precio de Venta (por unidad)', # Para registrar el precio de venta en ese momento
        }

# 3. Formulario en Línea (Formset)
# Crea un conjunto de formularios basados en Article, enlazados a Orders.
# extra=1 añade un formulario Article vacío por defecto.
# can_delete=True permite al usuario eliminar líneas de artículo.
ArticleFormSet = inlineformset_factory(
    Orders, 
    Article, 
    form=ArticleForm, 
    extra=1, 
    can_delete=True
)