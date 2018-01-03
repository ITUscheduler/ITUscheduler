from .serializers import CourseSerializer, CourseCodeSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView
from api.models import Course, CourseCode


class CourseListAPIView(ListAPIView):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class CourseDetailAPIView(RetrieveAPIView):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class CourseCodeDetailAPIView(RetrieveAPIView):
    serializer_class = CourseCodeSerializer
    queryset = CourseCode

