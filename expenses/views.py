from django.views.generic import ListView, UpdateView
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse

from .forms import ProductForm
from .models import Purchase, Product


def products_index(request):
    context = {
        'form': ProductForm(initial={'category': 1}),
        'products': Product.objects.all()
    }
    return render(request,
                  'expenses/products_index.html',
                  context)

def products_form(request):
    if request.method == 'POST':
        form = ProductForm(request.POST or None)
        if form.is_valid():
            product = form.save()
            return render(request,
                          'expenses/partials/product.html',
                          {'product': product})
        else:
            return render(request,
                          'expenses/partials/product_form.html',
                          {'form': form})
    return render(request,
                  'expenses/partials/product_form.html',
                  {'form': ProductForm()})


class PurchasesListView(ListView):
    model = Purchase
    context_object_name = "purchases"
    template_name = "expenses/purchases_list.html"


class PurchaseUpdateView(UpdateView):
    model = Purchase
    context_object_name = "purchase"
    template_name = "expenses/purchase_form.html"
    fields = ['datetime', 'place', 'note']

    def get_success_url(self):
        return reverse('index')
