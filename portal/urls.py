from django.urls import path
from . import views

app_name = 'portal'

urlpatterns = [
    path('', views.portal_login, name='login'),
    path('logout/', views.portal_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('job/<int:job_id>/', views.job_detail, name='job_detail'),
    path('job/<int:job_id>/invoice/', views.invoice, name='invoice'),
]
