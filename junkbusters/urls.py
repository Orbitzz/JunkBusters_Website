from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from website import oauth_views, marketing_auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('portal/', include('portal.urls', namespace='portal')),
    path('google-auth/start/', oauth_views.google_auth_start, name='google_auth_start'),
    path('google-auth/callback/', oauth_views.google_auth_callback, name='google_auth_callback'),
    path('google-auth/status/', oauth_views.google_auth_status, name='google_auth_status'),
    path('google-auth/clear-cache/', oauth_views.google_auth_clear_cache, name='google_auth_clear_cache'),
    path('marketing-auth/start/', marketing_auth_views.marketing_auth_start, name='marketing_auth_start'),
    path('marketing-auth/callback/', marketing_auth_views.marketing_auth_callback, name='marketing_auth_callback'),
    path('marketing-auth/telegram-id/', marketing_auth_views.marketing_telegram_id, name='marketing_telegram_id'),
    path('marketing-auth/run-report/', marketing_auth_views.marketing_run_report, name='marketing_run_report'),
    path('', include('website.urls', namespace='website')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
