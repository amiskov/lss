from django.urls import path

from .views import PurchaseUpdateView, PurchasesListView, products_index, \
    products_form, purchase_form, purchase_fill, expense_delete, \
    ProductUpdateView, product_delete

urlpatterns = [
    # path('?month=<month>', purchase_for_month, name='index_month'),
    path('', PurchasesListView.as_view(), name='index'),

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
