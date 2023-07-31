
from django.contrib import admin
from django.urls import path, include

from rest_framework import permissions

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
 
    path("auth/", include("user.urls"),),
    path('admin/', admin.site.urls),
   
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
