# from django.shortcuts import render

# # Create your views here.
# def customers(request):

#     return render(request, "customers.html", {
#         'title': 'Clientes'
#     })


from django.shortcuts import render, redirect, get_object_or_404
from .models import Customers
from .forms import CustomerForm

# R - READ (Listar Clientes)
def customer_list(request):
    # Obtiene todos los clientes y los ordena por apellido
    customers = Customers.objects.all().order_by('lastname', 'name')
    return render(request, 'customers/customer_list.html', {'customers': customers})

# C - CREATE (Crear Cliente)
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list') # Redirige a la lista después de crear
    else:
        form = CustomerForm()
    
    return render(request, 'customers/customer_form.html', {'form': form, 'title': 'Crear Cliente'})

# U - UPDATE (Actualizar Cliente)
def customer_update(request, pk):
    customer = get_object_or_404(Customers, pk=pk)
    
    if request.method == 'POST':
        # Instancia el formulario con los datos POST y la instancia existente (customer)
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_list') # Redirige a la lista después de actualizar
    else:
        # Instancia el formulario con los datos actuales del cliente para mostrarlos
        form = CustomerForm(instance=customer)
        
    return render(request, 'customers/customer_form.html', {'form': form, 'title': f'Editar Cliente: {customer.name}'})

# D - DELETE (Eliminar Cliente)
def customer_delete(request, pk):
    customer = get_object_or_404(Customers, pk=pk)
    
    if request.method == 'POST':
        customer.delete()
        return redirect('customer_list') # Redirige a la lista después de eliminar
    
    # Plantilla de confirmación de eliminación
    return render(request, 'customers/customer_confirm_delete.html', {'customer': customer})