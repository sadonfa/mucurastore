# from django.shortcuts import render

# Create your views here.
# def orders(request):

#     return render(request, "orders.html", {
#         'title': 'Pedidos'
#     })

from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from .forms import OrderForm, ArticleFormSet
from .models import Orders, Article
from django.http import JsonResponse, HttpResponse
from products.models import Products, Category
from decimal import Decimal 
import csv
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.decorators import login_required 

@login_required
def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        formset = ArticleFormSet(request.POST, instance=Orders()) # Se inicializa vacío para crear
        
        if form.is_valid() and formset.is_valid():
            try:
                # Usamos una transacción para asegurar que todo se guarda o nada se guarda
                with transaction.atomic():
                    # 1. Guardar el objeto Orders (el encabezado del pedido)
                    order_instance = form.save()
                    
                    # 2. Guardar el Formset de Articles, asociándolo al nuevo pedido
                    # commit=False es crucial si necesitas modificar los datos (ej: calcular el total)
                    articles = formset.save(commit=False)
                    
                    for article in articles:
                        # Asignar el pedido recién creado a cada artículo
                        article.order = order_instance
                        article.save()
                    
                    # Guardar artículos marcados para eliminación, si aplica
                    formset.save_m2m() # Si tuvieras campos ManyToMany
                    
                    return redirect('order_detail', pk=order_instance.pk) # Redirigir a la vista del pedido
            
            except Exception as e:
                # Manejar errores de base de datos o lógica aquí
                print(f"Error al guardar el pedido: {e}")
                # El formulario se volverá a renderizar con los errores
                
    else:
        # Petición GET: inicializar formularios vacíos
        form = OrderForm()
        formset = ArticleFormSet(instance=Orders())
    
    context = {
        'form': form,
        'formset': formset,
        'title': 'Crear Nuevo Pedido',
    }
    return render(request, 'orders/order_form.html', context)

@login_required
def addProducts(request):
    if request.method == 'POST':
        # 1. Obtener los datos POST
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        category_name = request.POST.get('category') # Nombre o ID de la categoría

        # 2. **BUSCAR EL OBJETO CATEGORY**
        try:
            # Asumiendo que category_name viene como el NOMBRE de la categoría
            category_instance = Category.objects.get(name=category_name)
        except Category.DoesNotExist:
            # Manejar el caso si la categoría no existe (opcional)
            # Podrías redirigir con un mensaje de error
            return render(request, 'products/add_product.html', {'error': 'Categoría no encontrada.'})

        # 3. Crear el nuevo producto
        try:
            Products.objects.create(
                name=name,
                description=description,
                price=price,
                stock=stock,
                # **ASIGNAR EL OBJETO INSTANCE, NO EL NOMBRE**
                category=category_instance 
            )
            return redirect('product_list') # Redirige a la lista de productos
        except Exception as e:
            # Manejar otros errores de creación
            return render(request, 'products/add_product.html', {'error': f'Error al guardar: {e}'})

    # Petición GET
    return render(request, 'products/add_product.html')

@login_required
def order_delete(request, pk):
    # 1. Obtener el pedido a eliminar
    order_instance = get_object_or_404(Orders, pk=pk)
    
    if request.method == 'POST':
        # Petición POST: Realizar la eliminación
        order_instance.delete()
        # Redirigir a la lista de pedidos después de eliminar
        return redirect('order_list') 
        
    # Petición GET: Mostrar la página de confirmación
    context = {
        'order': order_instance
    }
    # Usar una nueva plantilla para la confirmación
    return render(request, 'orders/order_confirm_delete.html', context)

@login_required
def order_detail(request, pk):
    order = get_object_or_404(Orders, pk=pk)
    articles = order.article_set.all() 
    
    total_pedido = Decimal(0) # Inicializar con Decimal para evitar errores de precisión

    for article in articles:
        # Calcular el subtotal y agregarlo como un atributo temporal al objeto Article
        # Usamos Decimal(article.cash) para asegurar que el cálculo es preciso
        article.subtotal = article.cash * Decimal(article.cantidad) 
        
        # Acumular al total general
        total_pedido += article.subtotal

    context = {
        'order': order,
        'articles': articles,
        'total_pedido': total_pedido, # Pasar el total calculado a la plantilla
    }
    
    return render(request, 'orders/order_detail.html', context)

@login_required
def order_update(request, pk):
    # Obtener el pedido existente o lanzar 404
    order_instance = get_object_or_404(Orders, pk=pk)
    
    if request.method == 'POST':
        # Instanciar formularios con los datos POST y la instancia existente
        form = OrderForm(request.POST, instance=order_instance)
        formset = ArticleFormSet(request.POST, instance=order_instance)
        
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                # 1. Guardar el objeto Orders (actualiza el encabezado)
                form.save()
                
                # 2. Guardar el Formset de Articles (actualiza, crea o elimina líneas)
                formset.save() 
                
                # Redirigir a la vista de detalle
                return redirect('order_detail', pk=order_instance.pk) 
            
    else:
        # Petición GET: Cargar formularios con los datos existentes
        form = OrderForm(instance=order_instance)
        formset = ArticleFormSet(instance=order_instance)
        
    context = {
        'form': form,
        'formset': formset,
        'title': f'Editar Pedido #{order_instance.pk}',
    }
    # Reutiliza la plantilla de formulario que usaste para crear el pedido.
    return render(request, 'orders/order_form.html', context)

@login_required
def order_finish_and_new(request, pk):
    # Asegúrate de que esta acción solo se realice con POST (según el formulario)
    if request.method == 'POST':
        order = get_object_or_404(Orders, pk=pk)
        
        # ----------------------------------------------------
        # LÓGICA DE FINALIZACIÓN DEL PEDIDO (si la necesitas)
        # ----------------------------------------------------
        
        try:
            with transaction.atomic():
                # **Aquí podrías añadir un campo 'status' a Orders 
                # y marcarlo como 'FINALIZADO' si tu modelo lo requiere**
                
                # Ejemplo de lógica de finalización:
                # order.status = 'FINALIZADO'
                # order.save()
                
                # **Opcional: Descontar el stock de los productos vendidos**
                for article in order.article_set.all():
                   product = article.product
                   product.stock -= article.cantidad
                   product.save()
                
                pass # Si no tienes lógica de finalización, puedes dejarlo pasar
        
        except Exception as e:
            # Manejar cualquier error crítico de la lógica (ej: stock negativo)
            return redirect('order_detail', pk=pk) 
            
        # ----------------------------------------------------
        
        # Redirigir SIEMPRE al formulario de creación de nuevo pedido
        return redirect('order_create')
        
    # Si alguien intenta acceder por GET, redirigir al detalle
    return redirect('order_detail', pk=pk)

@login_required
def get_product_price(request):
    product_id = request.GET.get('product_id')
    
    if product_id:
        try:
            # Obtener el producto o lanzar 404
            product = Products.objects.get(pk=product_id)
            
            # Devolver el precio como una respuesta JSON
            return JsonResponse({'price': str(product.price)})
        except Products.DoesNotExist:
            return JsonResponse({'error': 'Producto no encontrado'}, status=404)
            
    return JsonResponse({'error': 'ID de producto no proporcionado'}, status=400)


# R - READ (Listar Pedidos)
@login_required
def order_list(request):
    """Muestra una lista de todos los pedidos realizados."""

    date_str = request.GET.get('date')
    
    orders_queryset = Orders.objects.all().order_by('-created')
    selected_date = None
    total_sales = Decimal(0)

    if date_str:
        try:
            # 1. Convertir la cadena de fecha a un objeto date
            selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            
            # 2. Definir el inicio y fin del día (aware of timezones)
            start_of_day = timezone.make_aware(datetime.combine(selected_date, datetime.min.time()))
            end_of_day = timezone.make_aware(datetime.combine(selected_date, datetime.max.time()))
            
            # 3. Filtrar el queryset por el rango de tiempo
            orders_queryset = orders_queryset.filter(created__range=(start_of_day, end_of_day))
            
            # 4. Calcular el total de ventas de los pedidos filtrados
            for order in orders_queryset:
                # Itera sobre los artículos de cada orden para calcular el total
                for article in order.article_set.all():
                    subtotal = article.cash * Decimal(article.cantidad)
                    total_sales += subtotal
            
        except ValueError:
            # La fecha no es válida, no se aplica filtro
            pass
            
    context = {
        'orders': orders_queryset,
        'selected_date': selected_date.strftime('%Y-%m-%d') if selected_date else None,
        'total_sales': total_sales,
        'is_cierre': bool(date_str), # Usado en la plantilla para mostrar el resumen
    }
    
    
    # Obtener todos los pedidos y ordenarlos por fecha de creación (los más nuevos primero)
    # orders = Orders.objects.all().order_by('-created')
    
    # context = {
    #     'orders': orders,
    # }
    
    return render(request, 'orders/order_list.html', context)


@login_required
def export_orders_to_csv(request):
    # 1. Crear la respuesta HTTP con el tipo de contenido CSV
    response = HttpResponse(content_type='text/csv')
    
    # 2. Configurar el encabezado para forzar la descarga del archivo
    response['Content-Disposition'] = 'attachment; filename="listado_pedidos.csv"'

    # 3. Crear el escritor CSV
    writer = csv.writer(response)

    # 4. Escribir la fila de encabezados
    writer.writerow([
        'ID Pedido', 
        'Fecha Creacion', 
        'Nombre Cliente', 
        'Email Cliente', 
        'Titulo Pedido', 
        'Forma Pago'
    ])

    # 5. Obtener los datos y escribirlos
    orders = Orders.objects.all().order_by('-created')
    
    for order in orders:
        writer.writerow([
            order.pk,
            order.created.strftime("%Y-%m-%d %H:%M:%S"), # Formato la fecha/hora
            f"{order.cliente.name} {order.cliente.lastname}", # Nombre completo
            order.cliente.email,
            order.name,
            order.get_forma_pago_display(), # Usa el valor legible
        ])

    return response