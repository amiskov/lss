from django.contrib import admin

from .models import Income, IncomeSource


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('source_description', 'amount', 'source', 'datetime')
    autocomplete_fields = ['source']

    def source_description(self, obj: IncomeSource) -> str:
        return obj.description

    class Meta:
        ordering = ['-datetime', 'amount']


@admin.register(IncomeSource)
class IncomeSourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ['name', 'description']
