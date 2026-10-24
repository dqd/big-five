from django import template
from django.urls import translate_url

register = template.Library()


@register.simple_tag(takes_context=True)
def translate_current_url(context, language_code: str, absolute: bool = False) -> str:
    """Return the URL of the current page in the given language."""
    request = context["request"]
    url = translate_url(request.path, language_code)
    return request.build_absolute_uri(url) if absolute else url
