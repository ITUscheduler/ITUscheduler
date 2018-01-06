from rest_framework import serializers

from api.rest_api.serializers import CourseSerializer, CourseCodeSerializer

from scheduler.models import Schedule

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        exclude = ('courses', )