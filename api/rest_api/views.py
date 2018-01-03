from .serializers import CourseSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView
from api.models import Course


class CourseListAPIView(ListAPIView):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class CourseDetailAPIView(RetrieveAPIView):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


