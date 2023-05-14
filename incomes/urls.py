from django.urls import path


from .views import IncomesListView

urlpatterns = [
    path('', IncomesListView.as_view(), name='index'),
]
