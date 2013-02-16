from django.conf import settings


settings.configure(
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    ROOT_URLCONF = 'tests.urls',
    INSTALLED_APPS=[
        'activeurl',
    ],
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    }
)

if not 'django.core.context_processors.request' in settings.TEMPLATE_CONTEXT_PROCESSORS:
    settings.TEMPLATE_CONTEXT_PROCESSORS = list(settings.TEMPLATE_CONTEXT_PROCESSORS)
    settings.TEMPLATE_CONTEXT_PROCESSORS.append('django.core.context_processors.request')
