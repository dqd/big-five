from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = i18n_patterns(
    path(r"", include("bigfive.b5.urls")),
    prefix_default_language=False,
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL)
    urlpatterns.append(path("__debug__/", include("debug_toolbar.urls")))
