from django.urls import path

from .views import ScheduleListAPIView, ScheduleDetailAPIView, course_remove, course_replace

app_name = 'rest_api_scheduler'

urlpatterns = [
    path('list/', ScheduleListAPIView.as_view(), name='api_schedule_list'),
    path('detail/<int:pk>', ScheduleDetailAPIView.as_view(), name='api_schedule_detail'),
    path('course-remove/', course_remove, name='course_remove'),
    path('course-replace/', course_replace, name='course_replace'),
]