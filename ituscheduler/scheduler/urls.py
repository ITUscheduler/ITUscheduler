from django.urls import path

from . import views

urlpatterns = [
    # path('', views.shutdown, name="shutdown"),
    path('', views.IndexView.as_view(), name="index"),
    path('schedule/<int:pk>/', views.IndexView.as_view(), name="schedule"),
    path('share/<str:username>/', views.ScheduleView.as_view(), name="share"),
    path('signup/', views.RegistrationView.as_view(), name="signup"),
    path('courses/', views.CoursesView.as_view(), name="courses"),
    path('my-courses/remove/', views.remove_my_courses, name="remove_my_courses"),
    path('schedule/addCourse/', views.add_course, name="add_course"),
    path('schedule/select/', views.select_schedule, name="select_schedule"),
    path('schedule/delete/', views.delete_schedule, name="delete_schedule"),
    path('privacy-policy/', views.privacy_policy, name="privacy_policy"),
    path('sis/', views.sis, name="sis"),
    path('ads.txt/', views.ads, name="ads"),
    path('robots.txt/', views.robots, name="robots"),
    # path('schedule/removeCourse/<int:pk>/<int:pk>', views.remove_course, name='remove_course'),
    # path('schedule/replaceCourse', views.replace_course, name='replace_course'),
]
