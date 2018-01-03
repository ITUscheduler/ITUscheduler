from .views import CourseListAPIView, CourseDetailAPIView, CourseCodeListAPIView
from django.urls import path

app_name = 'course_api'

urlpatterns = [
    path('courses/<slug:course_code>', CourseListAPIView.as_view(), name='list_api'),
    path('detail/<int:pk>', CourseDetailAPIView.as_view(), name='list_detail'),
    path('course-codes', CourseCodeListAPIView.as_view(), name='course_code_list_api'),
]