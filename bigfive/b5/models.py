import string
from secrets import choice

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .constants import SLUG_LENGTH, AgeGroup, Sex
from .traits import DomainResult, build_report

SLUG_ALPHABET = string.ascii_lowercase + string.digits


def generate_slug() -> str:
    while True:
        slug = "".join(choice(SLUG_ALPHABET) for _ in range(SLUG_LENGTH))

        if not Answer.objects.filter(slug=slug).exists():
            return slug


class Answer(models.Model):
    slug = models.SlugField(default=generate_slug, max_length=SLUG_LENGTH, unique=True)
    sex = models.CharField(_("Your sex"), max_length=1, choices=Sex)
    age_group = models.CharField(_("Your age group"), max_length=1, choices=AgeGroup)
    # Percentile estimates keyed by the domain and facet keys, see ``traits``.
    results = models.JSONField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.slug

    def get_absolute_url(self) -> str:
        return reverse("result", args=(self.slug,))

    @property
    def report(self) -> list[DomainResult]:
        return build_report(self.results)
