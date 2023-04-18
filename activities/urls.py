from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:activity_id>/add/',
         views.add_acted_activity,
         name='add_acted_activity'),
    path('api/<int:activity_id>/add/',
         views.add_acted_activity_api,
         name='add_acted_activity_api'),
    path('<int:actedactivity_id>/remove/',
         views.remove_acted_activity,
         name='remove_acted_activity'),
]
