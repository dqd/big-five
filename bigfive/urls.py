from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path("", include("bigfive.b5.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL)
