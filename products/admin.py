from django.contrib import admin
from .models import Products, Category
# Register your models here.

class AdminCategory(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    list_display = ('name',  'created')

class AdminProducts(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    list_display = ('name',  'created')


admin.site.register(Category, AdminCategory)
admin.site.register(Products, AdminProducts)