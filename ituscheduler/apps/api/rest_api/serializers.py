from rest_framework import serializers

from ..models import (
    Course,
    MajorCode,
    Lecture,
    Prerequisite,
)


class MajorCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MajorCode
        fields = ('__all__')


class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        exclude = ('id',)


class PrerequisiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prerequisite
        exclude = ('id',)


class CourseSerializer(serializers.ModelSerializer):
    prerequisites = PrerequisiteSerializer

    class Meta:
        model = Course
        fields = ('__all__')
