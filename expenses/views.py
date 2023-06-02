from datetime import datetime

from django.db.models import QuerySet, Sum
from django.views.generic import UpdateView
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpRequest
from django.db.models import Q

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
            _ = form.save()
            return redirect('purchase_fill', pk)

    purchase = Purchase.objects \
        .select_related('place') \
        .prefetch_related('expenses__product') \
        .get(pk=pk)

    context = {
        'purchase_id': pk,
        'purchase': purchase,
        'products': Product.objects.select_related('category').all(),
        'form': ExpenseForm(initial={'purchase': pk})
    }
    return render(request,
                  'expenses/purchase_fill.html',
                  context)


def purchase_form(request: HttpRequest):
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


def purchases_index(request):
    queryset = Purchase.objects \
        .select_related('place') \
        .prefetch_related('expenses__product') \
        .annotate(Sum('expenses__price')) \
        .order_by('-datetime')

    place = request.GET.get('place', None)
    if place:
        queryset = queryset.filter(
            Q(place__name__icontains=place.capitalize())
        )

    month = request.GET.get('month', None)
    if month:
        queryset = queryset.filter(Q(datetime__month=month))

    # Must be after applying `month` and `place` to calculate totals accordingly
    totals = queryset.aggregate(Sum('expenses__price'))['expenses__price__sum']

    def get_type_totals(type: str) -> float:
        return queryset.filter(expenses__product__product_type=type) \
            .aggregate(Sum('expenses__price'))['expenses__price__sum'] or 0

    context = {
        'purchases': queryset,
        'totals': {
            'sum': totals or 0,
            'bad': get_type_totals('bad'),
            'good': get_type_totals('good'),
            'necessary': get_type_totals('necessary'),
        },
    }
    return render(request,
                  'expenses/purchases_table.html',
                  context)


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
