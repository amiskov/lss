from django.urls import path
from django.urls import path

from . import views

urlpatterns = [
    # Activities
    path('activities/form/',
         views.add_activity_form,
         name='add_activity'),


    # Acted Activities
    path('', views.index, name='index'),
    path('<int:activity_id>/add/',
         views.add_acted_activity,
         name='add_acted_activity'),
    path('<pk>/edit/',
         views.ActedUpdateView.as_view(),
         name='edit_acted_activity'),
    path('api/<int:activity_id>/add/',
         views.add_acted_activity_api,
         name='add_acted_activity_api'),
    path('<int:actedactivity_id>/remove/',
         views.remove_acted_activity,
         name='remove_acted_activity'),

    # Acted Activity Time
    path('<pk>/show_time',
         views.show_time,
         name='show_time'),
    path('<pk>/change_time',
         views.change_time,
         name='change_time_form'),
]
