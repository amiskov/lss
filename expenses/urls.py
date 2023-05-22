from django.urls import path

from .views import PurchaseUpdateView, PurchasesListView, products_index, \
    products_form

urlpatterns = [
    path('', PurchasesListView.as_view(), name='index'),
    path('products/', products_index, name='products_index'),
    path('products/create/', products_form, name='products_form'),
    path('<pk>/edit/',
         PurchaseUpdateView.as_view(),
         name='edit_purchase'),
]
