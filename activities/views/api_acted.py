from django.http.response import HttpResponse
from django.contrib import messages
from django.shortcuts import redirect

from rest_framework.generics import ListAPIView

from ..serializers import ActivitySerializer
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
