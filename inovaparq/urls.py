from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('inovaparq/', include('startups.urls', namespace='startups')),
    path('inovaparq/', include('django.contrib.auth.urls')),
]
