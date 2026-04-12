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
    path('sitemap.xml', views.sitemap, name='sitemap'),
    path('robots.txt', views.robots, name='robots'),
    # City landing pages — before catch-all
    path('junk-removal-clarksville/', views.city_clarksville, name='city_clarksville'),
    path('junk-removal-bowling-green/', views.city_bowling_green, name='city_bowling_green'),
    path('kentucky/', views.city_kentucky, name='city_kentucky'),
    # Individual service pages — must come last (catch-all slug)
    path('<slug:slug>/', views.service_page, name='service_page'),
]
