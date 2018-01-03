from django.urls import path
from api import views

urlpatterns = [
    path('refresh/courses', views.RefreshCoursesView.as_view(), name="refresh_courses"),
    path('db/refresh/course_codes', views.db_refresh_course_codes, name="db_refresh_course_codes"),
    path('db/refresh/courses', views.db_refresh_courses, name="db_refresh_courses"),
    path('db/flush', views.db_flush, name="db_flush"),
    path('course_codes', views.get_course_codes, name="api_course_codes"),
    path('courses', views.get_courses, name="api_courses")
]
