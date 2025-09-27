# from django.urls import path
# from .views import orders

# urlpatterns = [
#     path('pedidos/', orders, name="orders"),
# ]


from django.urls import path
from . import views

urlpatterns = [
    # CREATE - Vista para crear un nuevo pedido (y sus artículos)
    path('pedidos/new/', views.create_order, name='order_create'),
    path('api/price/', views.get_product_price, name='api_get_price'),
    
    # También necesitarías una vista para ver el detalle del pedido (order_detail)
    path('pedidos/<int:pk>/', views.order_detail, name='order_detail'), 
    path('pedidos/<int:pk>/edit/', views.order_update, name='order_update'),   

    path('pedidos/<int:pk>/finish/', views.order_finish_and_new, name='order_finish_and_new'),  
    path('pedidos/', views.order_list, name='order_list'),

    path('export/csv/', views.export_orders_to_csv, name='order_export_csv'),
    # URL de Eliminación 
    # path('pedidos/<int:pk>/delete/', views.order_delete, name='order_delete'),
    
    # ... otras URLs para listar pedidos, etc.
]