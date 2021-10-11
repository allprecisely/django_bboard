from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.views import serve
from django.urls import include
from django.urls import path
from django.views.decorators.cache import never_cache

urlpatterns = [path('admin/', admin.site.urls), path('', include('main.urls'))]

if settings.DEBUG:
    urlpatterns.append(path('static/<path:path>', never_cache(serve)))
