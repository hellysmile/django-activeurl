from django.conf import settings  # noqa
from appconf import AppConf


class ActiveUrlConf(AppConf):
    '''default settings for django-activeurl'''

    # flipper for caching feature
    CACHE = True

    # django cache expiration time
    CACHE_TIMEOUT = 60 * 60 * 24

    # django cache key prefix
    CACHE_PREFIX = 'django_activeurl'

    # dict with default template tag kwargs
    KWARGS = {
        'css_class': 'active',
        'parent_tag': 'li',
        'menu': 'yes'
    }

    class Meta:
        prefix = 'active_url'
