from django.urls import path
from . import views

urlpatterns = [
    path('refresh/courses', views.RefreshCoursesView.as_view(), name="refresh_courses"),
    path('flush', views.FlushView.as_view(), name="flush"),
    path('db/refresh/major_codes', views.db_refresh_major_codes, name="db_refresh_major_codes"),
    path('db/refresh/courses', views.db_refresh_courses, name="db_refresh_courses"),
    path('db/refresh/courses/<str:task_id>/', views.TaskStatusView.as_view(), name="task_status"),
    path('db/flush', views.db_flush, name="db_flush")
]
