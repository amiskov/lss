import datetime as dt
import re

from django.http.response import HttpResponse, HttpResponseBadRequest
from django.contrib import messages
from django.shortcuts import redirect

from rest_framework.generics import ListAPIView
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ..serializers import ActedActivitySerializer, ActivitySerializer
from ..models import ActedActivity, Activity


class ActivitiesAPIView(ListAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer


def add_acted_activity_api(request, activity_id):
    if request.method == "GET":
        added_acted_activity = ActedActivity.add(activity_id)
        return HttpResponse(
            f"{added_acted_activity.activity.name} was added successfully!"
        )
    else:
        messages.error(request, f"Use GET method.")
        return redirect('index')


class ActedActivityViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        q = ActedActivity.objects \
            .select_related('activity') \
            .prefetch_related('tag')

        if 'date' not in self.request.GET:
            d = dt.date.today()
        else:
            raw_date = self.request.GET['date']
            if raw_date == 'today':
                d = dt.date.today()
            elif re.match(r'^\d{4}-\d{2}-\d{2}$', raw_date):
                d = dt.date.fromisoformat(self.request.GET['date'])
            else:
                return HttpResponseBadRequest()

        d_min = dt.datetime.combine(d, dt.time.min)
        d_max = dt.datetime.combine(d, dt.time.max)
        q = q.filter(started__range=(d_min, d_max))
        return q.all()

    serializer_class = ActedActivitySerializer
