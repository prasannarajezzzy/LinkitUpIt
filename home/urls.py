
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('', include('about.urls')),
    path('', include('contact.urls')),
    path('', include('login.urls')),
]
