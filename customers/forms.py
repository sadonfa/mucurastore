from django import forms
from .models import Customers

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customers
        # Incluimos todos los campos del modelo Customers
        fields = ['name', 'lastname', 'email', 'movil']
        
        labels = {
            'name': 'Nombre',
            'lastname': 'Apellidos',
            'email': 'Correo Electrónico',
            'movil': 'Teléfono/Móvil',
        }