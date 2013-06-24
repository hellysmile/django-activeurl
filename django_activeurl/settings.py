'''default settings for django-activeurl'''
from django.conf import settings


# flipper for caching feature
ACTIVE_URL_CACHE = getattr(
    settings, 'ACTIVE_URL_CACHE', True
)

# django cache expiration time
ACTIVE_URL_CACHE_TIMEOUT = getattr(
    settings, 'ACTIVE_URL_CACHE_TIMEOUT', 60 * 60 * 24
)

# django cache key prefix
ACTIVE_URL_CACHE_PREFIX = getattr(
    settings, 'ACTIVE_URL_CACHE_PREFIX', 'django_activeurl'
)

# dict with default template tag kwargs
ACTIVE_URL_KWARGS = getattr(
    settings, 'ACTIVE_URL_KWARGS', {
        'css_class': 'active',
        'parent_tag': 'li',
        'menu': 'yes'
    }
)
