from django.urls import path

from .views import PurchaseUpdateView, products_index, \
    products_form, purchase_form, purchase_fill, expense_delete, \
    product_delete, purchases_index

urlpatterns = [
    # path('?month=<month>', purchase_for_month, name='index_month'),
    path('', purchases_index, name='purchases_index'),

    # Product
    path('products/', products_index, name='products_index'),
    path('products/create/', products_form, name='products_form'),
    path('products/<pk>/delete/', product_delete, name='product_delete'),
    path('products/<pk>/edit/', products_form, name='product_edit'),

    # Expense
    path('expense/<pk>/delete/', expense_delete, name='expense_delete'),

    # Purchase
    path('purchase/create/', purchase_form, name='purchase_form'),
    path('purchase/<pk>/fill/', purchase_fill, name='purchase_fill'),
    path('<pk>/edit/',
         PurchaseUpdateView.as_view(),
         name='edit_purchase'),
]
