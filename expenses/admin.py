from django.contrib import admin
from .models import Expense, Place, Product, Category, Purchase


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('product', 'price', 'purchase', 'id')
    autocomplete_fields = ['product', 'purchase']
    # list_filter = ('name', 'amount')

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('datetime', 'place', 'note', 'id')
    search_fields = ['place', 'note', 'datetime']


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')
    search_fields = ['name', 'address']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    search_fields = ['name']
    
