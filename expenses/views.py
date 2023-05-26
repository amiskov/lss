from datetime import datetime

from django.views.generic import ListView, UpdateView
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse

from .forms import ProductForm, PurchaseForm, ExpenseForm
from .models import Purchase, Product, Place, Expense


def product_delete(request, pk):
    if request.method == 'POST':
        p = Product.objects.get(pk=pk)
        p.delete()
        return HttpResponse('')
    return HttpResponse('Method should be post.')


def expense_delete(request, pk):
    if request.method == 'POST':
        expense = Expense.objects.get(pk=pk)
        expense.delete()
        return HttpResponse('')
    return HttpResponse('Method should be post.')


def purchase_fill(request, pk):
    if request.method == 'POST':
        form = ExpenseForm(request.POST or None)
        if form.is_valid():
            expense = form.save()
            return redirect('purchase_fill', pk)

    context = {
        'purchase_id': pk,
        'purchase': Purchase.objects.get(pk=pk),
        'products': Product.objects.all(),
        'form': ExpenseForm(initial={
            'purchase': pk,
        })
    }
    return render(request,
                  'expenses/purchase_fill.html',
                  context)


def purchase_form(request):
    if request.method == 'POST':
        form = PurchaseForm(request.POST or None)
        if form.is_valid():
            purchase = form.save()
            return redirect('purchase_fill', purchase.pk)

    context = {
        'form': PurchaseForm(initial={
            'datetime': datetime.now(),
            'place': 1,
        }),
        'places': Place.objects.all()
    }
    return render(request,
                  'expenses/purchase_form.html',
                  context)


def products_index(request):
    context = {
        'form': ProductForm(initial={'category': 1}),
        'products': Product.objects.all()
    }
    return render(request,
                  'expenses/products_index.html',
                  context)


def products_form(request, pk=None):
    if request.method == 'POST':
        # Save Product view
        form = ProductForm(request.POST or None)
        if form.is_valid():
            product = form.save()
            print(product.pk)
            return render(request,
                          'expenses/partials/product.html',
                          {'product': product})
        else:
            return render(request,
                          'expenses/partials/product_form.html',
                          {'form': form})
    elif request.method == 'GET' and pk:
        # Update Product view
        product = Product.objects.get(pk=pk)
        return render(request,
                      'expenses/partials/product_form.html',
                      {'form': ProductForm(instance=product)})
    else:
        # Create Product view
        return render(request,
                      'expenses/partials/product_form.html',
                      {'form': ProductForm()})


class PurchasesListView(ListView):
    model = Purchase
    context_object_name = "purchases"
    template_name = "expenses/purchases_list.html"

    def get_context_data(self, **kwargs):
        context = super(PurchasesListView, self).get_context_data(**kwargs)
        queryset = self.get_queryset()
        totals = 0
        for pur in queryset.all():
            print(pur.totals)
            totals += pur.totals
        context['totals'] = totals
        return context

    def get_queryset(self):
        if self.request.method == 'GET':
            queryset = Purchase.objects.all()
            month = self.request.GET.get('month', None)
            if month is not None:
                queryset = queryset.filter(datetime__month=month)
            return queryset


class PurchaseUpdateView(UpdateView):
    model = Purchase
    context_object_name = "purchase"
    template_name = "expenses/purchase_form.html"
    fields = ['datetime', 'place', 'note']

    def get_success_url(self):
        return reverse('index')


class ProductUpdateView(UpdateView):
    model = Product
    context_object_name = "product"
    template_name = "expenses/partials/product_form.html"
    fields = ['name', 'category']

    def get_success_url(self):
        return reverse('products_index')
