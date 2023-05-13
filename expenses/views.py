from django.shortcuts import render
from django.views.generic import ListView

from expenses.models import Purchase


class PurchasesListView(ListView):
    model = Purchase
    context_object_name = "purchases"
    template_name = "expenses/purchases_list.html"


# class ActedUpdateView(UpdateView):
#     model = ActedActivity
#     fields = ["started", "finished", "note", "tag"]
#     context_object_name = "acted"
#     template_name = "activities/acted_form.html"

#     def get_success_url(self):
#         return reverse('index')
