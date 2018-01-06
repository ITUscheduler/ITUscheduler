from django.urls import path

from .views import ScheduleListAPIView, ScheduleDetailAPIView

app_name = 'rest_api_scheduler'

urlpatterns = [
    path('list/', ScheduleListAPIView.as_view(), name='api_schedule_list'),
    path('detail/<int:pk>', ScheduleDetailAPIView.as_view(), name='api_schedule_detail'),
]