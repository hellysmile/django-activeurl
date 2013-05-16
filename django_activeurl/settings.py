from django.conf import settings


CACHE_ACTIVE_URL = getattr(
    settings, 'CACHE_ACTIVE_URL', True
)

CACHE_ACTIVE_URL_TIMEOUT = getattr(
    settings, 'CACHE_ACTIVE_URL_TIMEOUT', 60 * 60 * 24
)

CACHE_ACTIVE_URL_PREFIX = getattr(
    settings, 'CACHE_ACTIVE_URL_PREFIX', 'django_activeurl.'
)

DEFAULT_KWARGS = {
    'css_class': 'active',
    'parent_tag': 'li'
}
