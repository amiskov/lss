from django.views.generic import ListView

from expenses.models import Purchase


class PurchasesListView(ListView):
    model = Purchase
    context_object_name = "purchases"
    template_name = "expenses/purchases_list.html"
