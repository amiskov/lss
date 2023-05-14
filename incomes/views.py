from django.views.generic import ListView
from django.db.models import Sum

from .models import Income


class IncomesListView(ListView):
    model = Income
    context_object_name = "incomes"
    template_name = "incomes/incomes_list.html"

    # def get_queryset(self):
    #     queryset = Model_Item.objects.all()
    #     queryset = queryset.annotate(
    #             sum_ = Sum(When(model_itemtransaction__item_sold))
    #         )
    #     return queryset

    # def _get_totals(self):
    #     totals = 0
    #     for e in self.amount:
    #         totals += e.price
    #     return totals


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        totals = 0
        for i in context['object_list']:
            print(i, totals)
            totals += i.amount
        context['totals'] = totals
        return context

