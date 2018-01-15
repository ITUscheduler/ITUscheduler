from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('accounts/reset-password', auth_views.PasswordResetView.as_view(), name="password-reset"),
    path('accounts/reset-password-done', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('accounts/reset-password-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/reset-password-complete', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('', include('scheduler.urls')),
    path('api/', include('api.urls')),
    path('rest-api/', include('api.rest_api.urls', namespace='course_api')),
    path('schedules-rest-api/', include('scheduler.rest_api.urls', namespace='rest_api_scheduler')),
]
