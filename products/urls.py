# from django.urls import path
# from .views import products, formProducts,addProducts, updateProducts

# urlpatterns = [
#     path('productos/', products, name="products"),
#     path('formulario/', formProducts, name="formulario" ),
#     path('add-product/', addProducts, name="addproduct" ),
#     path('update-product/<int:id>/', updateProducts, name="updateproduct" ),
# ]


from django.urls import path
from . import views

urlpatterns = [
    # READ
    path('productos/', views.product_list, name='product_list'),
    # path('productos/', views.products, name="products"),
    
    # CREATE
    path('new/', views.product_create, name='product_create'),
    
    # UPDATE
    # 'pk' (Primary Key) es el ID del producto que queremos editar
    path('edit/<int:pk>/', views.product_update, name='product_update'),
    
    # DELETE
    path('delete/<int:pk>/', views.product_delete, name='product_delete'),
]