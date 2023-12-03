from django.urls import path, re_path

from . import views
from .constants import SLUG_LENGTH

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    re_path(
        f"^(?P<slug>[a-z0-9]{{{SLUG_LENGTH}}})/$",
        views.ResultView.as_view(),
        name="result",
    ),
]
