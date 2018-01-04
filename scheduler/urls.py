from django.conf.urls import url
from scheduler import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name="index"),
    url(r'^schedule/(?P<id>\d+)/$', views.IndexView.as_view(), name="schedule"),
    url(r'^signup/$', views.RegistrationView.as_view(), name="signup"),
    url(r'^courses/(?P<slug>[\w-]+)$', views.CoursesView.as_view(), name="courses"),
    url(r'^schedule/addCourse/$', views.add_course, name="add_course"),
    url(r'^schedule/select/$', views.select_schedule, name="select_schedule"),
    url(r'^schedule/removeCourse/$', views.remove_course, name='remove_course'),
    url(r'^schedule/replaceCourse/$', views.replace_course, name='replace_course'),
]
