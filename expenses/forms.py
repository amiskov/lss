from django.forms import HiddenInput, ModelForm, TextInput, DateTimeInput
from .models import Product, Purchase, Expense


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'category')
        widgets = {
            'name': TextInput(
                attrs={'autofocus': 'true',
                       'autocomplete': 'off',
                       # There should be `datalist` tag with products
                       # having `id='existingProducts'`
                       'list': 'existingProducts'},),
        }


class PurchaseForm(ModelForm):
    class Meta:
        model = Purchase
        fields = ('place', 'datetime', 'note')
        widgets = {
            'place': TextInput(
                attrs={'autofocus': 'true',
                       'autocomplete': 'off',
                       'list': 'existingPlaces'}),
            'datetime': DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M',
            ),
        }

class ExpenseForm(ModelForm):
    class Meta:
        model = Expense
        fields = ('product', 'price', 'purchase')
        widgets = {
            'purchase': HiddenInput(),
            'product': TextInput(
                attrs={'autofocus': 'true',
                       'autocomplete': 'off',
                       'list': 'existingProducts'},)
        }
