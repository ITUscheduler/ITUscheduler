from django.conf.urls import url
from api import views

urlpatterns = [
    url(r'^refresh/courses/$', views.RefreshCoursesView.as_view(), name="refresh_courses"),
    url(r'^db/refresh/course_codes/$', views.db_refresh_course_codes, name="db_refresh_course_codes"),
    url(r'^db/refresh/courses/$', views.db_refresh_courses, name="db_refresh_courses"),
    url(r'^db/flush/$', views.db_flush, name="db_flush"),
    url(r'^course_codes/$', views.get_course_codes, name="api_course_codes"),
    url(r'^courses/$', views.get_courses, name="api_courses")
]
