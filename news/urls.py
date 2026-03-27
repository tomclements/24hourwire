from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required
from . import views
from .views_dashboard import dashboard_view

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about_view, name='about'),
    path('terms/', views.terms_view, name='terms'),
    path('privacy/', views.privacy_view, name='privacy'),
    path('dashboard/', staff_member_required(dashboard_view), name='dashboard'),
]
