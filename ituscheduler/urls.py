from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from django.urls import (
    path,
    include,
)

from ituscheduler.apps.api.models import MajorCode
from .sitemaps import (
    StaticViewSitemap,
    IndexViewSitemap,
)
from .views import empty

urlpatterns = [
                  path('health/', empty),
                  path('admin/', admin.site.urls),
                  path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
                  path('accounts/logout', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
                  path('accounts/reset-password', auth_views.PasswordResetView.as_view(), name="password-reset"),
                  path('accounts/reset-password-done', auth_views.PasswordResetDoneView.as_view(),
                       name="password_reset_done"),
                  path('accounts/reset-password-confirm/<uidb64>/<token>/',
                       auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
                  path('accounts/reset-password-complete', auth_views.PasswordResetCompleteView.as_view(),
                       name='password_reset_complete'),
                  path('sitemap.xml', sitemap, {
                      'sitemaps': {
                          'home': IndexViewSitemap,
                          'pages': StaticViewSitemap,
                          'courses': GenericSitemap({
                                                        "queryset": MajorCode.objects.all()
                                                    }, priority=0.7)
                      }
                  }, name='django.contrib.sitemaps.views.sitemap'),
                  path('oauth/', include('social_django.urls', namespace='social')),
                  path('', include('ituscheduler.apps.scheduler.urls')),
                  path('api/', include('ituscheduler.apps.api.urls')),
                  path('rest-api/', include('ituscheduler.apps.api.rest_api.urls', namespace='course_api')),
                  path('schedules-rest-api/',
                       include('ituscheduler.apps.scheduler.rest_api.urls', namespace='rest_api_scheduler')),
                  path('info/', include('ituscheduler.apps.blog.urls', namespace='info')),
                  path('celery-progress/', include('celery_progress.urls'))
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
