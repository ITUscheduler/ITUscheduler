from django.conf.urls import url
from scheduler import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name="index"),
    url(r'^signup/$', views.RegistrationView.as_view(), name="signup")
]