from django.shortcuts import render

from ..forms import ActivityForm
from ..models import Activity


def add_activity_button(request):
    return render(request, 'activities/_partials/add_activity_button.html')


def add_activity_form(request):
    if request.method == "GET":
        return render(request,
                      'activities/_partials/activity_form.html',
                      {'form': ActivityForm})
    if request.method == 'POST':
        form = ActivityForm(request.POST or None)

        if form.is_valid():
            _ = form.save()
        return render(request,
                      'activities/_partials/activities_list.html',
                      {'activities': Activity.objects.order_by('activity_type')})
