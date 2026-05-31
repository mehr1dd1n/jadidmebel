from django.conf import settings
from django.urls import translate_url
from django.utils import translation

from .models import SiteSettings


def site_settings(request):
    settings_obj, _ = SiteSettings.objects.get_or_create(pk=1)
    return {'settings': settings_obj}


def language_switcher(request):
    current = translation.get_language() or settings.LANGUAGE_CODE
    languages = []
    for code, label in settings.LANGUAGES:
        try:
            url = translate_url(request.path, code) if request.path else f'/{code}/'
        except Exception:
            url = f'/{code}/'
        languages.append({
            'code': code,
            'label': label,
            'url': url,
            'active': current[:2] == code,
        })
    return {
        'current_language': current[:2],
        'language_choices': languages,
    }
