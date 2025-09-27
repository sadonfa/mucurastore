from django import forms
from .models import Products

class ProductForm(forms.ModelForm):
    # La descripción en tu modelo Products es un CharField con max_length=150.
    # Si quieres que sea un campo de texto multi-línea (como un <textarea> en HTML), 
    # puedes forzarlo aquí usando widgets.
    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        max_length=250, # Puedes ajustar el max_length si es necesario
        required=False
    )
    
    class Meta:
        model = Products
        # 'fields' debe incluir todos los campos que el usuario va a editar.
        # El campo 'id' se genera automáticamente. 'created' y 'updated'
        # se gestionan automáticamente en el modelo.
        fields = ['name', 'description', 'price', 'stock', 'category']
        
        # Opcional: Personalizar las etiquetas
        labels = {
            'name': 'Nombre del Producto',
            'description': 'Descripción',
            'price': 'Precio ($)',
            'stock': 'Stock',
            'category': 'Categoría',
        }