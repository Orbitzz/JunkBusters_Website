from django.urls import path
from . import views

app_name = 'website'

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('quote/', views.quote, name='quote'),
    path('quote/success/', views.quote_success, name='quote_success'),
    path('book/', views.booking, name='booking'),
    path('book/success/', views.booking_success, name='booking_success'),
    path('areas-we-serve/', views.areas, name='areas'),
    path('gallery/', views.gallery, name='gallery'),
    path('contact/', views.contact, name='contact'),
    path('loyalty/', views.loyalty, name='loyalty'),
    path('track/', views.track, name='track'),
    path('referral/', views.referral, name='referral'),
    path('api/chat/', views.chat_proxy, name='chat_proxy'),
    path('api/chat/poll/', views.chat_poll, name='chat_poll'),
    path('sitemap.xml', views.sitemap, name='sitemap'),
    path('robots.txt', views.robots, name='robots'),
    # City landing pages — before catch-all
    path('junk-removal-clarksville/', views.city_clarksville, name='city_clarksville'),
    path('junk-removal-bowling-green/', views.city_bowling_green, name='city_bowling_green'),
    path('kentucky/', views.city_kentucky, name='city_kentucky'),
    path('junk-removal-nashville/', views.city_nashville, name='city_nashville'),
    path('junk-removal-white-house-tn/', views.city_white_house, name='city_white_house'),
    path('junk-removal-hendersonville-tn/', views.city_hendersonville, name='city_hendersonville'),
    path('junk-removal-gallatin-tn/', views.city_gallatin, name='city_gallatin'),
    path('junk-removal-springfield-tn/', views.city_springfield, name='city_springfield'),
    path('junk-removal-franklin-tn/', views.city_franklin, name='city_franklin'),
    path('junk-removal-goodlettsville-tn/', views.city_goodlettsville, name='city_goodlettsville'),
    path('junk-removal-portland-tn/', views.city_portland, name='city_portland'),
    # Individual service pages — must come last (catch-all slug)
    path('<slug:slug>/', views.service_page, name='service_page'),
]
