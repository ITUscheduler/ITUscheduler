from django.conf.urls import url
from api import views

urlpatterns = [
    url(r'^refresh/course_codes/$', views.refresh_course_codes, name="refresh_course_codes"),
    url(r'^refresh/courses/$', views.refresh_courses, name="refresh_courses")
]