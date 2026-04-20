from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'portal'

urlpatterns = [
    path('',            views.portal_login,    name='login'),
    path('register/',   views.portal_register, name='register'),
    path('logout/',     views.portal_logout,   name='logout'),
    path('dashboard/',  views.dashboard,        name='dashboard'),
    path('profile/',    views.profile_view,     name='profile'),
    path('password/',   views.password_change,  name='password_change'),

    # Email verification
    path('verify/sent/',              views.verify_sent,          name='verify_sent'),
    path('verify/resend/',            views.resend_verification,  name='resend_verification'),
    path('verify/<uidb64>/<token>/',  views.verify_email,         name='verify_email'),

    # Password reset flow
    path('forgot/',
         auth_views.PasswordResetView.as_view(
             template_name='portal/password_reset_request.html',
             email_template_name='portal/password_reset_email.txt',
             subject_template_name='portal/password_reset_subject.txt',
             success_url='/portal/forgot/sent/',
         ), name='password_reset'),
    path('forgot/sent/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='portal/password_reset_sent.html',
         ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='portal/password_reset_confirm.html',
             success_url='/portal/reset/done/',
         ), name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='portal/password_reset_complete.html',
         ), name='password_reset_complete'),
]
