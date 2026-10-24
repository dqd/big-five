from django.db.models import IntegerChoices, TextChoices
from django.utils.translation import gettext_lazy as _

SLUG_LENGTH = 8

# Percentile boundaries: a score below LOW_SCORE counts as low, a score above
# HIGH_SCORE as high. Roughly the lowest 30 % and the highest 30 % of people.
LOW_SCORE = 45
HIGH_SCORE = 55


class Sex(TextChoices):
    FEMALE = "F", _("Female")
    MALE = "M", _("Male")


class AgeGroup(TextChoices):
    YOUNG = "Y", _("20 years old or younger")
    ADULTS = "A", _("21–40 years old")
    MATURE = "M", _("41–60 years old")
    ELDERLY = "E", _("61 years old or older")


class Response(IntegerChoices):
    VERY_ACCURATE = 5, _("Very accurate")
    ACCURATE = 4, _("Moderately accurate")
    NEUTRAL = 3, _("Neither accurate nor inaccurate")
    INACCURATE = 2, _("Moderately inaccurate")
    VERY_INACCURATE = 1, _("Very inaccurate")


class Level(TextChoices):
    LOW = "low", _("low")
    AVERAGE = "average", _("average")
    HIGH = "high", _("high")

    @classmethod
    def of(cls, score: int) -> "Level":
        if score < LOW_SCORE:
            return cls.LOW
        if score > HIGH_SCORE:
            return cls.HIGH
        return cls.AVERAGE
