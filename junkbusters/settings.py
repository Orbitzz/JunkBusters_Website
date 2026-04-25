import os
from pathlib import Path
from decouple import config, Csv

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())

# Google APIs
GOOGLE_MAPS_API_KEY = config('GOOGLE_MAPS_API_KEY', default='')
GOOGLE_PLACE_ID = config('GOOGLE_PLACE_ID', default='')
GOOGLE_OAUTH_CLIENT_ID = config('GOOGLE_OAUTH_CLIENT_ID', default='')
GOOGLE_OAUTH_CLIENT_SECRET = config('GOOGLE_OAUTH_CLIENT_SECRET', default='')
GOOGLE_OAUTH_REDIRECT_URI = config('GOOGLE_OAUTH_REDIRECT_URI', default='http://localhost:8001/google-auth/callback/')

# FieldCommand integration
FIELDCOMMAND_REVIEWS_URL   = config('FIELDCOMMAND_REVIEWS_URL',   default='http://127.0.0.1:8000/marketing/api/widget/reviews/')
FIELDCOMMAND_EMBED_URL     = config('FIELDCOMMAND_EMBED_URL',     default='http://127.0.0.1:8000/marketing/api/embed/{endpoint}/')
FIELDCOMMAND_EMBED_API_KEY = config('FIELDCOMMAND_EMBED_API_KEY', default='')

# Google review URL
GOOGLE_REVIEW_URL = config('GOOGLE_REVIEW_URL', default='https://g.page/r/CaQvxFrtKJyzEBM/review')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'website',
    'portal',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'website.middleware.UTMCaptureMiddleware',
]

ROOT_URLCONF = 'junkbusters.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'website' / 'templates', BASE_DIR / 'portal' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'website.context_processors.business_info',
                'website.context_processors.google_reviews',
            ],
        },
    },
]

WSGI_APPLICATION = 'junkbusters.wsgi.application'

import dj_database_url
import sentry_sdk

SENTRY_DSN = config('SENTRY_DSN', default='')
if SENTRY_DSN:
    sentry_sdk.init(dsn=SENTRY_DSN, traces_sample_rate=0.2)

# Twilio (SMS for job status notifications)
TWILIO_ACCOUNT_SID = config('TWILIO_ACCOUNT_SID', default='')
TWILIO_AUTH_TOKEN  = config('TWILIO_AUTH_TOKEN',  default='')
TWILIO_FROM_NUMBER = config('TWILIO_FROM_NUMBER', default='')
DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
    )
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Chicago'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SESSION_COOKIE_AGE = 86400
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# HTTPS / production security
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
CSRF_TRUSTED_ORIGINS    = config('CSRF_TRUSTED_ORIGINS', default='', cast=Csv())
SESSION_COOKIE_SECURE   = not DEBUG
CSRF_COOKIE_SECURE      = not DEBUG

BUSINESS_NAME = 'Junk Busters LLC'
BUSINESS_PHONE = '615-881-2505'
BUSINESS_EMAIL = 'info@junkbustershauling.com'
BUSINESS_ADDRESS = 'Orlinda, TN (serving Middle TN & Southern KY)'

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
EMAIL_TIMEOUT = 8
DEFAULT_FROM_EMAIL = config('EMAIL_HOST_USER', default='')
CONTACT_EMAIL = config('CONTACT_EMAIL', default='c.thompson@junkbusters.info')
