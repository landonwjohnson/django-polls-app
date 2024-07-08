# mysite/urls.py

from django.contrib import admin
from django.urls import path, include, re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('polls/', include('polls.urls')),  
    path('api/', include('jobs.urls')),     


]
