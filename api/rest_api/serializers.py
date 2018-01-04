from rest_framework import serializers
from api.models import Course, CourseCode, Lecture


class CourseCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCode
        fields = ('__all__')


class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ('__all__')


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('__all__')




