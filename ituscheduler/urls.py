from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include

from ituscheduler.api.models import MajorCode
from .sitemaps import StaticViewSitemap, IndexViewSitemap
from .views import health_check

urlpatterns = [
    path('health/', health_check),
    path('admin/', admin.site.urls),
    # auth
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('accounts/reset-password/', auth_views.PasswordResetView.as_view(), name='password-reset'),
    path(
        route='accounts/reset-password-done/',
        view=auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done',
    ),
    path(
        route='accounts/reset-password-confirm/<uidb64>/<token>/',
        view=auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm',
    ),
    path(
        route='accounts/reset-password-complete/',
        view=auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete',
    ),
    path(
        route='sitemap.xml/',
        view=sitemap,
        kwargs={
            'sitemaps': {
                'home': IndexViewSitemap,
                'pages': StaticViewSitemap,
                'courses': GenericSitemap({'queryset': MajorCode.objects.all()}, priority=0.7),
            },
        },
        name='django.contrib.sitemaps.views.sitemap',
    ),
    # social auth
    path('oauth/', include('social_django.urls', namespace='social')),
    # celery
    path('celery-progress/', include('celery_progress.urls')),
    # apps and apis
    path('api/', include('ituscheduler.api.urls')),
    path('rest-api/', include('ituscheduler.api.rest_api.urls', namespace='course_api')),
    path('schedules-rest-api/', include('ituscheduler.scheduler.rest_api.urls', namespace='rest_api_scheduler')),
    path('info/', include('ituscheduler.blog.urls', namespace='info')),
    path('', include('ituscheduler.scheduler.urls')),
]
