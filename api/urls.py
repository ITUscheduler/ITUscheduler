from django.conf.urls import url
from api import views

urlpatterns = [
    url(r'^db/refresh/$', views.db_refresh, name="db_refresh"),
    url(r'^db/flush/$', views.db_flush, name="db_flush"),
    url(r'^course_codes/$', views.get_course_codes, name="api_course_codes"),
    url(r'^courses/$', views.get_courses, name="api_courses")
]
