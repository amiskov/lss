from django.urls import path, include
from django.urls import path
from rest_framework import routers
from rest_framework.routers import SimpleRouter

from activities.views.api_acted import ActedActivityViewSet

from . import views

# DRF urls
router = SimpleRouter()
# router.register("api/acted/<str:day>", ActedActivityViewSet, basename="api_acted_for_day")
router.register("api/acted", ActedActivityViewSet, basename="api_acted")
# router.register(r'(?P<date>\d{4}-\d{2}-\d{2})', ActedActivityViewSet, basename="api_acted")


urlpatterns = [
    # Activities
    path('activities/form/',
         views.add_activity_form,
         name='add_activity'),
    path('activities/add_button/',
         views.add_activity_button,
         name='add_activity_button'),

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
] + router.urls

