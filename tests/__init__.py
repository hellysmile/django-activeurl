# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os

import django
from django.conf import settings

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

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
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'APP_DIRS': True,
        'DIRS': [os.path.join(PROJECT_ROOT, 'templates/jinja')],
        'OPTIONS': {
            'environment': 'tests.jinja_config.environment',
        },
    },
]

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
    TEMPLATES=template_engines,
)

settings.configure(**config)

django.setup()
