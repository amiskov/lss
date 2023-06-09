from datetime import date, timedelta
from collections import defaultdict

import humanize
from humanize import precisedelta
from dateutil.relativedelta import relativedelta

from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone, dateparse
from django.views.generic import UpdateView
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.timezone import get_current_timezone
from django.views.decorators.csrf import csrf_protect

from ..models import ActedActivity, Activity
from ..forms import ActivityForm

from .acted import *
from .activities import *
from .api_acted import *



def index(request):
    activities = Activity.objects.order_by('activity_type')

    date_param: str | None = request.GET.get('date')
    query_date: date = (date_param and dateparse.parse_date(date_param)) \
        or timezone.localdate()

    last_day: date = query_date + relativedelta(day=31)  # won't exceed 31
    month_days = [(dt :=date(query_date.year, query_date.month, d),
                   humanize.naturaldate(dt))
                  for d in range(1, last_day.day)]

    _, acted = ActedActivity.get_acted_for_day(query_date)

    activity_types_totals = defaultdict(int)
    # acted activities grouped and sorted by total duration
    activities_totals = defaultdict(timedelta)
    names_with_types = defaultdict(str)

    for a in acted:
        activities_totals[a.activity.name] += a.duration
        names_with_types[a.activity.name] = a.activity.activity_type
        activity_types_totals[a.activity.activity_type] += a.duration.seconds

    # must be non zero
    total_seconds = max(sum(activity_types_totals.values()), 1)

    percents_by_type = defaultdict(int)
    # Alphabetically sorted by labels
    for k, v in sorted(activity_types_totals.items(), key=lambda e: e[0]):
        percents_by_type[k] = round(v / total_seconds * 100)

    # TODO: Don't store data in `acted`, pass it separately
    labels = str(list(percents_by_type.keys()))
    values = str(list(percents_by_type.values()))
    total_seconds = total_seconds

    # sort by duration
    durs_sorted = list(activities_totals.items())
    durs_sorted.sort(key=lambda d: d[1].seconds, reverse=True)

    # humanize and add activity type
    durs = []
    for d in durs_sorted:
        name, dur = d
        t = (name, precisedelta(dur, minimum_unit="minutes",
                                format="%0.0f"), names_with_types[name])
        durs.append(t)

    context = {
        'query_date': query_date,
        'labels': labels,
        'totals': durs,
        'values': values,
        'activities': activities,
        'acted_activities': acted,
        'month_days': month_days
    }

    if request.htmx:
        return render(request, 'activities/partial.html', context)
    else:
        return render(request, 'activities/index.html', context)


