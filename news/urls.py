from django.urls import path
from django.contrib.auth.decorators import login_required, user_passes_test
from . import views
from .views_dashboard import dashboard_view
from .feeds import GlobalFeed, LanguageFeed, CategoryFeed, JSONFeedView

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about_view, name='about'),
    path('terms/', views.terms_view, name='terms'),
    path('privacy/', views.privacy_view, name='privacy'),
    path('copyright/', views.copyright_view, name='copyright'),
    path('dashboard/', user_passes_test(views.is_staff_or_superuser, login_url='/login/')(dashboard_view), name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('different-angle/<int:story_id>/', views.different_angle, name='different_angle'),
    path('story/<int:story_id>/', views.story_share, name='story_share'),
    # RSS Feeds
    path('feed/', GlobalFeed(), name='feed_global'),
    path('feed/<str:language>/', LanguageFeed(), name='feed_language'),
    path('feed/<str:language>/<str:category>/', CategoryFeed(), name='feed_category'),
    # JSON Feeds
    path('feed.json', JSONFeedView.as_view(), name='feed_json_global'),
    path('feed/<str:language>.json', JSONFeedView.as_view(), name='feed_json_language'),
    path('feed/<str:language>/<str:category>.json', JSONFeedView.as_view(), name='feed_json_category'),
]
