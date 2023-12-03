from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag(takes_context=True)
def language_url(context, code_new, code_current):
    path = (
        context["request"].path
        if settings.LANGUAGE_CODE == code_current
        else context["request"].path[3:]
    )
    prefix = "" if settings.LANGUAGE_CODE == code_new else f"/{code_new}"

    return prefix + path
