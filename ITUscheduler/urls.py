from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('', include('scheduler.urls')),
    path('api/', include('api.urls')),
    path('rest-api/', include('api.rest_api.urls', namespace='rest_api')),
    path('schedules-rest-api/', include('scheduler.rest_api.urls', namespace='rest_api_scheduler')),
]
