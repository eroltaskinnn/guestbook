# project/urls.py
from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include('app.urls')),  # Include the app's URLs
]