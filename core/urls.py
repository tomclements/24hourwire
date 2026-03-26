from django.contrib import admin
from django.urls import path, include
from news import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('fetch/', views.fetch_news_trigger, name='fetch_news_trigger'),
    path('', include('news.urls')),
]
