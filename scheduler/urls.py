from django.urls import path
from scheduler import views

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('schedule/<int:pk>', views.IndexView.as_view(), name="schedule"),
    path('signup', views.RegistrationView.as_view(), name="signup"),
    path('courses/<slug:slug>', views.CoursesView.as_view(), name="courses"),
    path('contact', views.contact, name="contact"),
    path('schedule/addCourse', views.add_course, name="add_course"),
    path('schedule/select', views.select_schedule, name="select_schedule"),
    path('schedule/delete', views.delete_schedule, name="delete_schedule"),
    #path('schedule/removeCourse/<int:pk>/<int:pk>', views.remove_course, name='remove_course'),
    #path('schedule/replaceCourse', views.replace_course, name='replace_course'),
]
