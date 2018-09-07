from django.urls import path
from scheduler import views

urlpatterns = [
    path('', views.shutdown, name="index"),
    # path('', views.IndexView.as_view(), name="index"),
    path('schedule/<int:pk>', views.IndexView.as_view(), name="schedule"),
    path('share/<str:username>/', views.ScheduleView.as_view(), name="share"),
    path('signup', views.RegistrationView.as_view(), name="signup"),
    path('courses', views.CoursesView.as_view(), name="courses"),
    path('contact/', views.contact, name="contact"),
    path('my-courses/remove', views.remove_my_courses, name="remove_my_courses"),
    path('schedule/addCourse', views.add_course, name="add_course"),
    path('schedule/select', views.select_schedule, name="select_schedule"),
    path('schedule/delete', views.delete_schedule, name="delete_schedule"),
    path('schedule', views.schedule_export, name="schedule_export"),
    path('schedule/generator', views.schedule_generate, name="schedule_generator"),
    path('schedule.png', views.ScheduleExportView.as_view(), name="schedule_png"),
    path('schedule.pdf', views.ScheduleExportView.as_view(), name="schedule_pdf"),
    path('privacy-policy', views.privacy_policy, name="privacy_policy"),

    #path('schedule/removeCourse/<int:pk>/<int:pk>', views.remove_course, name='remove_course'),
    #path('schedule/replaceCourse', views.replace_course, name='replace_course'),
]
