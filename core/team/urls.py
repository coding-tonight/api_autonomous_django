from django.urls import path 
from django.conf import settings
from django.conf.urls import static

urlpatterns = [
#  path('team/')
] + static(settings.MEDIA_URL,  document_root=settings.MEDIA_ROOT)