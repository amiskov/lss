from collections import defaultdict
from django.db import models
from django.db.models.fields.related import ForeignKey
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import timedelta, datetime, time
from humanize import precisedelta


class Activity(models.Model):
    name = models.CharField(max_length=512)

    class Meta:
        verbose_name_plural = "Activities"

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

    def add(activity_id):
        activity = Activity.objects.get(id=activity_id)
        acted_activity = ActedActivity(
            finished=timezone.now(),
            activity=activity)
        acted_activity.save()
        return acted_activity

    def get_acted_for_day(day: datetime):
        acted = ActedActivity.objects.filter(
            # only today after 5 AM:
            finished__year=day.year,
            finished__month=day.month,
            finished__day=day.day,
            finished__hour__gte=5,
        ).order_by('-finished')
        seconds_by_type = defaultdict(int)

        duration_by_name = defaultdict(timedelta)
        names_with_types = defaultdict(str)

        for i, today_activity in enumerate(acted):
            is_earliest = (i == len(acted) - 1)

            duration = timedelta(seconds=0) if is_earliest \
                else (today_activity.finished - acted[i + 1].finished)

            duration_by_name[today_activity.activity.name] += duration
            names_with_types[today_activity.activity.name] = today_activity.activity.activity_type

            seconds_by_type[today_activity.activity.activity_type] += duration.seconds

            today_activity.duration = precisedelta(
                duration, minimum_unit="minutes", format="%0.0f")

        # must be non zero
        total_seconds = max(sum(seconds_by_type.values()), 1)

        percents_by_type = defaultdict(int)
        # Alphabetically sorted by labels
        for k, v in sorted(seconds_by_type.items(), key=lambda e: e[0]):
            percents_by_type[k] = round(v / total_seconds * 100)

        acted.all = str(dict(percents_by_type))
        acted.day = day
        acted.labels = str(list(percents_by_type.keys()))
        acted.values = str(list(percents_by_type.values()))
        acted.total_seconds = total_seconds

        # sort by duration
        durs_sorted = list(duration_by_name.items())
        durs_sorted.sort(key=lambda d: d[1].seconds, reverse=True)

        # humanize and add activity type
        durs = []
        for d in durs_sorted:
            name, dur = d
            t = (name, precisedelta(dur, minimum_unit="minutes", format="%0.0f"), names_with_types[name])
            durs.append(t)

        acted.totals = durs
        acted.names_with_types = names_with_types
        return acted

    @classmethod
    def acted_today(cls):
        today = timezone.now()
        return cls.get_acted_for_day(today)

    class Meta:
        verbose_name_plural = "Acted Activities"

    def __str__(self):
        return self.activity.name + ", " + self.finished.strftime("%y-%m-%d %H:%M")