from django.urls import path
from . import views

app_name = 'website'

# Legacy slug 301s are handled inside views.service_page via the
# LEGACY_REDIRECTS dict in views.py. That path serves both slash and
# no-slash forms because the catch-all <slug:slug>/ pattern below covers
# any historical URL Google indexed, then service_page 301s to the
# current slug. Prior URL-pattern-based redirects only matched the
# no-slash form and 404'd on Google's with-slash URLs.

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
    path('api/availability/', views.availability_proxy, name='availability_proxy'),
    path('api/chat/', views.chat_proxy, name='chat_proxy'),
    path('api/chat/poll/', views.chat_poll, name='chat_poll'),
    path('api/service-area-map/', views.service_area_geojson, name='service_area_geojson'),
    path('api/embed/member-signup/', views.member_signup_webhook, name='member_signup_webhook'),
    path('sitemap.xml', views.sitemap, name='sitemap'),
    path('robots.txt', views.robots, name='robots'),
    path('llms.txt', views.llms_txt, name='llms_txt'),
    path('health/', views.health, name='health'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('pricing/', views.pricing, name='pricing'),
    path('faq/', views.faq, name='faq'),
    # City landing pages — before catch-all. 15 city pages + /kentucky/ hub
    # were removed in the 2026-08-17 consolidation and now 301 to their
    # nearest surviving hub via LEGACY_REDIRECTS in service_page.
    path('junk-removal-nashville/', views.city_nashville, name='city_nashville'),
    path('junk-removal-white-house-tn/', views.city_white_house, name='city_white_house'),
    path('junk-removal-hendersonville-tn/', views.city_hendersonville, name='city_hendersonville'),
    path('junk-removal-gallatin-tn/', views.city_gallatin, name='city_gallatin'),
    path('junk-removal-springfield-tn/', views.city_springfield, name='city_springfield'),
    path('junk-removal-goodlettsville-tn/', views.city_goodlettsville, name='city_goodlettsville'),
    path('junk-removal-portland-tn/',       views.city_portland,       name='city_portland'),
    path('junk-removal-franklin-ky/',       views.city_franklin_ky,    name='city_franklin_ky'),
    # Gift cards
    path('gift-card/',          views.gift_card_purchase, name='gift_card'),
    path('gift-card/success/',  views.gift_card_success,  name='gift_card_success'),
    path('gift-card/webhook/',  views.gift_card_webhook,  name='gift_card_webhook'),
    path('gift-card/check/',    views.gift_card_check,    name='gift_card_check'),
    # Individual service pages — must come last (catch-all slug).
    # Also handles all legacy 301 redirects via LEGACY_REDIRECTS dict lookup
    # inside service_page (see views.py).
    path('<slug:slug>/', views.service_page, name='service_page'),
]
