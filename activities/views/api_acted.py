import datetime as dt

from django.http.response import HttpResponse
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
        if 'date' in self.request.GET:
            d = dt.date.fromisoformat(self.request.GET['date'])
            d_min = dt.datetime.combine(d, dt.time.min)
            d_max = dt.datetime.combine(d, dt.time.max)
            # Invoice.objects.get(user=user, date__range=(today_min, today_max))
            q = q.filter(started__range=(d_min, d_max))
        return q.all()

    serializer_class = ActedActivitySerializer
