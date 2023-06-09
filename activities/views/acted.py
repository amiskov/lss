from django.http import HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseServerError
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import UpdateView
from django.utils import dateparse
from django.utils.timezone import get_current_timezone

from ..models import ActedActivity


class ActedUpdateView(UpdateView):
    model = ActedActivity
    fields = ["started", "finished", "note", "tag"]
    context_object_name = "acted"
    template_name = "activities/acted_form.html"

    def get_success_url(self):
        return reverse('index')


def add_acted_activity(request, activity_id):
    _added = ActedActivity.add(activity_id)
    # messages.success(request,
    #                  f"<b>{added.activity.name}</b> was added successfully!")
    return redirect('index')


def remove_acted_activity(request, actedactivity_id):
    acted_activity = ActedActivity.objects.get(id=actedactivity_id)
    _activity_name = acted_activity.activity.name
    acted_activity.delete()
    # messages.success(
    #     request, f"<b>{activity_name}</b> was removed successfully!")
    return redirect('index')


def show_time(request, pk):
    acted = ActedActivity.objects.get(pk=pk)
    return render(
        request, 'activities/_time.html', context={'acted': acted}
    )


def change_time(request, pk):
    acted = ActedActivity.objects.get(pk=pk)
    if request.method == 'POST':
        tz = get_current_timezone()

        # TODO: update time in separate function
        new_started_time = dateparse.parse_time(request.POST['started'])
        new_finished_time = dateparse.parse_time(request.POST['finished'])

        if not new_started_time or not new_finished_time:
            return HttpResponseServerError()

        current_started_time = acted.started.astimezone(tz)
        current_finished_time = acted.finished.astimezone(tz)

        # start must be less than finish
        if current_started_time > current_finished_time:
            # TODO: show a message, not an error
            return HttpResponseBadRequest()

        new_started = current_started_time.replace(
            hour=new_started_time.hour,
            minute=new_started_time.minute
        )
        new_finished = current_finished_time.replace(
            hour=new_finished_time.hour,
            minute=new_finished_time.minute
        )
        acted.started, acted.finished = new_started, new_finished
        acted.save(update_fields=["started", "finished"])

        if request.htmx:
            return redirect('index')
    return render(
        request, 'activities/time_form.html', context={'acted': acted}
    )
