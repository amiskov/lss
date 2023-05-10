from django.contrib import admin
from .models import Activity, ActedActivity, Tag


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'activity_type', 'id')
    list_filter = ('activity_type', )


@admin.register(ActedActivity)
class ActedActivityAdmin(admin.ModelAdmin):
    list_display = ('activity', 'started', 'finished', 'id')
    list_filter = ('finished', )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name', )