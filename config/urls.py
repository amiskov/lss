from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('activities.urls')),
    path('expenses/', include('expenses.urls')),
    path('incomes/', include('incomes.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
] + staticfiles_urlpatterns()
