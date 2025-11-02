# from django.shortcuts import redirect, render
# from .models import Products, Category

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Products, Category
from .forms import ProductForm
from django.contrib.auth.decorators import login_required 


# Create your views here.
@login_required
def products(request):

    products = Products.objects.all()

    return render(request, "productos.html", {
        'title': 'Productos',
        'products': products 
    })

@login_required
def formProducts(request):

    categories = Category.objects.all()

    return render(request, 'formulario.html', {
        'title': 'Formulario',
        'categories': categories
    })

@login_required
def addProducts(request):

    name = request.POST['nombre']
    description = request.POST['descripcion'] 
    price = request.POST['precio'] 
    stock = request.POST['stock']
    category_value = request.POST['categoria']  

    # print(category)
    print(price)

    try:
        # Opción A: Buscar por NOMBRE (si en el formulario envías el nombre, como "Bebidas")
        category_instance = Category.objects.get(name=category_value)
        
        # Opción B: Buscar por ID (si en el formulario envías el ID de la categoría, como 1)
        # Descomenta y usa esta opción si estás seguro de que envías el ID:
        # category_instance = get_object_or_404(Category, id=category_value)
    
    except Category.DoesNotExist:
        # Manejar el caso si la categoría no existe (opcional pero recomendado)
        # Podrías mostrar un error o redirigir
        return render(request, 'error.html', {'message': f"La categoría '{category_value}' no existe."})


    product = Products(
            name = name,
            description = description,
            price = price,
            stock = stock,
            category = category_instance
        )

    product.save()

    return redirect('/productos/')

@login_required
def updateProducts(request, id):

    product = Products.objects.get(id=id)

    # product.name = request.POST['nombre']
    # description = request.POST['descripcion'] 
    # price = request.POST['precio'] 
    # product.stock = request.POST['stock']
    # category_value = request.POST['categoria']  


    return render(request, 'formulario.html', {
        'title': 'Actualizacion de producto',
        'product': product,
        'valor': 'update'
    })




# IA


# C - CREATE (Crear Producto)
@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirigir a la lista de productos después de guardar
            return redirect('product_list')
    else:
        form = ProductForm()
    
    # Usaremos la misma plantilla para crear y editar
    return render(request, 'product_form.html', {'form': form, 'title': 'Crear Producto'})


# R - READ (Listar Productos)
@login_required
def product_list(request):
    products = Products.objects.all().order_by('name')
    return render(request, 'product_list.html', {'products': products})


# U - UPDATE (Actualizar Producto)
@login_required
def product_update(request, pk):
    # Obtener el producto o lanzar 404 si no existe
    product = get_object_or_404(Products, pk=pk)
    
    if request.method == 'POST':
        # Instanciar el formulario con los datos POST y la instancia existente
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            # Redirigir a la lista de productos después de actualizar
            return redirect('product_list')
    else:
        # Instanciar el formulario con los datos actuales del producto
        form = ProductForm(instance=product)
        
    return render(request, 'product_form.html', {'form': form, 'title': 'Editar Producto'})


# D - DELETE (Eliminar Producto)
@login_required
def product_delete(request, pk):
    product = get_object_or_404(Products, pk=pk)
    if request.method == 'POST':
        product.delete()
        # Redirigir a la lista de productos después de eliminar
        return redirect('product_list')
    
    # Plantilla de confirmación
    return render(request, 'product_confirm_delete.html', {'product': product})



