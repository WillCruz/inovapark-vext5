from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('inovapark/', include('startups.urls', namespace='startups')),
]