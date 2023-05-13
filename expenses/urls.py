from django.urls import path


from .views import PurchasesListView

urlpatterns = [
    path('', PurchasesListView.as_view(), name='index'),
]
