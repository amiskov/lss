from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'category')
        widgets = {
            'name': forms.TextInput(
                attrs={'autofocus': 'true',
                       'autocomplete': 'off',
                       # There should be `datalist` tag with products
                       # having `id='existingProducts'`
                       'list': 'existingProducts'},),
        }
