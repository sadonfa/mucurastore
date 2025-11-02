# from django.urls import path
# from .views import customers

# urlpatterns = [
#     path('clientes/', customers, name="customers"),
# ]

from django.urls import path
from . import views

urlpatterns = [
    # READ
    path('clientes/', views.customer_list, name='customer_list'),
    
    # CREATE
    path('new-customer/', views.customer_create, name='customer_create'),
    
    # UPDATE
    path('edit-customer/<int:pk>/', views.customer_update, name='customer_update'),
    
    # DELETE
    path('delete-customer/<int:pk>/', views.customer_delete, name='customer_delete'),
]