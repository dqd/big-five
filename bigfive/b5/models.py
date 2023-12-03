import string
from secrets import choice

from django.db import models
from django.utils.translation import gettext_lazy as _

from .constants import SLUG_LENGTH, Sex, AgeGroup


def generate_slug():
    while True:
        alphabet = string.ascii_lowercase + string.digits
        slug = "".join(choice(alphabet) for _ in range(SLUG_LENGTH))

        if not Answer.objects.filter(slug=slug).exists():
            return slug


class Answer(models.Model):
    slug = models.SlugField(
        default=generate_slug,
        max_length=SLUG_LENGTH,
        unique=True,
        db_index=True,
    )
    sex = models.CharField(
        verbose_name=_("Your sex"),
        max_length=1,
        choices=Sex.choices,
    )
    age_group = models.CharField(
        verbose_name=_("Your age group"),
        max_length=1,
        choices=AgeGroup.choices,
    )
    results = models.JSONField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.slug
