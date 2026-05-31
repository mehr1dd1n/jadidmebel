from django.utils import translation


SUPPORTED = ('uz', 'ru', 'en')


def get_lang():
    lang = (translation.get_language() or 'uz')[:2]
    return lang if lang in SUPPORTED else 'uz'


def get_translated(instance, field):
    """Mahsulot/kategoriya maydonini joriy tilda qaytaradi."""
    lang = get_lang()
    for code in (lang, 'uz', 'ru', 'en'):
        val = getattr(instance, f'{field}_{code}', None)
        if val:
            return val
    return ''
