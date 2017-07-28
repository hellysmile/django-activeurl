from __future__ import absolute_import, unicode_literals

import os

from django.conf import settings


PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))


config = dict(
    ALLOWED_HOSTS=['testserver'],
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        },
    },
    ROOT_URLCONF='tests.urls',
    CACHES={
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        },
    },
)

try:
    # django >= 1.8
    from django.template import engines  # noqa

    template_engines = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'APP_DIRS': True,
            'DIRS': [os.path.join(PROJECT_ROOT, 'templates/django')],
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.request',
                ],
            },
        },
    ]

    try:
        # is jinja installed ?
        import jinja2  # noqa

        template_engines.append({
            'BACKEND': 'django.template.backends.jinja2.Jinja2',
            'APP_DIRS': True,
            'DIRS': [os.path.join(PROJECT_ROOT, 'templates/jinja')],
            'OPTIONS': {
                'environment': 'tests.jinja_config.environment',
            },
        })
    except ImportError:
        pass

    config.update(
        TEMPLATES=template_engines,
    )
except ImportError:
    config.update(
        TEMPLATE_CONTEXT_PROCESSORS=[
            'django.core.context_processors.request',
        ],
        TEMPLATE_DIRS=[os.path.join(PROJECT_ROOT, 'templates/django')],
    )

settings.configure(**config)

try:
    # django 1.7 standalone app setup
    import django
    django.setup()
except AttributeError:
    pass
