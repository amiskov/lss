from __future__ import annotations
from datetime import date, timedelta

from humanize import precisedelta

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class Activity(models.Model):
    name = models.CharField(max_length=512)

    class Meta:
        verbose_name_plural = _("Activities")

    class Type(models.TextChoices):
        GOOD = "good", _('Good')
        BAD = "bad", _('Bad')
        NECESSARY = "necessary", _('Necessary')

    activity_type = models.CharField(
        max_length=56,
        choices=Type.choices,
        default=Type.NECESSARY,
    )

    def __str__(self):
        return self.name


class ActedActivity(models.Model):
    started = models.DateTimeField('action started')
    finished = models.DateTimeField('action finished')
    activity = models.ForeignKey(Activity, on_delete=models.RESTRICT)
    note = models.CharField(max_length=1024)

    @property
    def duration(self) -> timedelta:
        return self.finished - self.started

    @property
    def duration_for_humans(self) -> str:
        return precisedelta(
            self.duration,
            minimum_unit="minutes", format="%0.0f"
        )

    @staticmethod
    def add(activity_id: str) -> ActedActivity:
        activity = Activity.objects.get(id=activity_id)
        prev_acted = ActedActivity.objects.last()

        started = timezone.now()
        if prev_acted and (timezone.now() - prev_acted.finished < timedelta(days=1)):
            started = prev_acted.finished

        acted_activity = ActedActivity(
            started=started,
            finished=timezone.now(),
            activity=activity)
        acted_activity.save()
        return acted_activity

    @staticmethod
    def get_acted_for_day(day: date):
        acted = ActedActivity.objects.filter(
            # only today after 5 AM:
            finished__year=day.year,
            finished__month=day.month,
            finished__day=day.day,
            finished__hour__gte=5,
        ).order_by('-finished')
        return (day, acted)

    class Meta:
        verbose_name_plural = _("Acted Activities")

    def __str__(self) -> str:
        return self.activity.name + ", " + \
            self.started.strftime("%y-%m-%d %H:%M") + "-" + \
            self.finished.strftime("%y-%m-%d %H:%M")
