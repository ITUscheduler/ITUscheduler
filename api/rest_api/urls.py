from .views import CourseListAPIView, CourseDetailAPIView
from django.urls import path

app_name = 'course_api'

urlpatterns = [
    path('list/', CourseListAPIView.as_view(), name='list_api'),
    path('detail/<int:pk>', CourseDetailAPIView.as_view(), name='list_detail'),
]