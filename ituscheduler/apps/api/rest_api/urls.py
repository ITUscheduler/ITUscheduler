from .views import CourseListAPIView, CourseDetailAPIView, MajorCodeListAPIView
from django.urls import path

app_name = 'course_api'

urlpatterns = [
    path('courses/<slug:major_code>', CourseListAPIView.as_view(), name='list_api'),
    path('detail/', CourseDetailAPIView.as_view(), name='list_detail'),
    path('major-codes', MajorCodeListAPIView.as_view(), name='major_code_list_api'),
]