from .serializers import CourseSerializer, CourseCodeSerializer, LectureSerializer, PrerequisiteSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from api.models import Course, CourseCode


class CourseListAPIView(ListAPIView):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        code = kwargs['course_code']
        course_code = get_object_or_404(CourseCode, code=code)
        queryset = queryset.filter(course_code=course_code)

        if request.GET.get('code'):
            code = request.GET['code']
            queryset = queryset.filter(code=code)

        data = [(self.get_serializer(query).data, query) for query in queryset]

        response_data = []

        for serializer, query in data:
            serializer['lectures'] = LectureSerializer(query.lecture_set.all(), many=True).data
            serializer['prerequisites'] = PrerequisiteSerializer(query.prerequisites.all(), many=True).data
            response_data.append(serializer)

        return Response(response_data)


class CourseDetailAPIView(RetrieveAPIView):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance).data
        serializer['lectures'] = LectureSerializer(instance.lecture_set.all(), many=True).data
        serializer['prerequisites'] = PrerequisiteSerializer(instance.prerequisites.all(), many=True).data

        return Response(serializer)


class CourseCodeListAPIView(ListAPIView):
    queryset = CourseCode.objects.all()
    serializer_class = CourseCodeSerializer


