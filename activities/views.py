from datetime import datetime, date

import humanize
from dateutil.relativedelta import relativedelta

from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.utils import timezone, dateparse
from django.views.generic import ListView

from .models import ActedActivity, Activity


def index(request):
    activities = Activity.objects.order_by('activity_type')

    date_param = request.GET.get('date')
    query_date = dateparse.parse_date(
        date_param) if date_param else timezone.now()

    last_day: datetime = query_date + relativedelta(day=31)  # won't exceed 31
    month_days = [(dt :=date(query_date.year, query_date.month, d), humanize.naturaldate(dt))
                  for d in range(1, last_day.day)]

    context = {
        'activities': activities,
        'acted_activities': ActedActivity.get_acted_for_day(query_date),
        'month_days': month_days
    }

    return render(request, 'activities/index.html', context)


def add_acted_activity(request, activity_id):
    added = ActedActivity.add(activity_id)
    messages.success(request,
                     f"<b>{added.activity.name}</b> was added successfully!")
    return redirect('index')


def add_acted_activity_api(request, activity_id):
    if request.method == "GET":
        added_acted_activity = ActedActivity.add(activity_id)
        return HttpResponse(f"{added_acted_activity.activity.name} was added successfully!")
    else:
        messages.error(request, f"Use GET method.")
        return redirect('index')


def remove_acted_activity(request, actedactivity_id):
    acted_activity = ActedActivity.objects.get(id=actedactivity_id)
    activity_name = acted_activity.activity.name
    acted_activity.delete()
    messages.success(
        request, f"<b>{activity_name}</b> was removed successfully!")
    return redirect('index')
