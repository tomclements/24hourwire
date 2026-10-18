from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include
from django.views.decorators.http import require_safe

ADS_TXT = 'google.com, pub-1306415581374425, DIRECT, f08c47fec0942fa0\n'


@require_safe
def ads_txt(request):
    return HttpResponse(ADS_TXT, content_type='text/plain; charset=utf-8')


urlpatterns = [
    path('ads.txt', ads_txt, name='ads_txt'),
    path('admin/', admin.site.urls),
    path('', include('news.urls')),
]
