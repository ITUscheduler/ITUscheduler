from rest_framework import serializers
from api.models import Course, CourseCode, Lecture, Prerequisite


class CourseCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCode
        fields = ('__all__')


class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        exclude = ('id', )


class PrerequisiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prerequisite
        fields = ('__all__')


class CourseSerializer(serializers.ModelSerializer):
    prerequisites = PrerequisiteSerializer
    class Meta:
        model = Course
        fields = ('__all__')





