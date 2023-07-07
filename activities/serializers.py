from rest_framework import serializers

from .models import Activity, ActedActivity


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ("id", "name", "activity_type")


class ActedActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ActedActivity
        fields = ("id", "activity_name", "activity_type", "started", "finished", "note", "tag")
