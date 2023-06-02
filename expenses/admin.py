from django.contrib import admin
from .models import Expense, Place, Product, Category, Purchase, Sum
from djmoney.models.fields import Money


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('product', 'price', 'purchase', 'id')
    autocomplete_fields = ['product', 'purchase']
    # TODO: add filter by totals diapasons. E.g. 0—1000₽, up to 1000—3000₽ etc.
    list_filter = ('purchase__place', )


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('datetime', 'place', 'totals', 'note', 'id')
    search_fields = ['place', 'note', 'datetime']

    def get_queryset(self, request):
        queryset = super(PurchaseAdmin, self).get_queryset(request)
        return queryset.annotate(totals=Sum('expenses__price'))

    def totals(self, obj):
        return Money(obj.totals, 'RUB')


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')
    search_fields = ['name', 'address']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_type', 'category')
    search_fields = ['name']
