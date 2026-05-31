from django import template
from django.urls import translate_url
from django.conf import settings

from main.translations import translate
from main.i18n_utils import get_translated

register = template.Library()


@register.simple_tag(takes_context=True)
def t(context, key):
    return translate(key)


@register.filter
def tfield(obj, field):
    if obj is None:
        return ''
    if hasattr(obj, 'get_t'):
        return obj.get_t(field)
    return get_translated(obj, field)


@register.filter
def mat_label(code):
    return translate(f'mat.{code}')


@register.simple_tag(takes_context=True)
def lang_url(context, lang_code):
    request = context.get('request')
    if not request:
        return f'/{lang_code}/'
    try:
        return translate_url(request.path, lang_code)
    except Exception:
        return f'/{lang_code}/'
