# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from jinja2 import Environment

from django_activeurl.ext.django_jinja import ActiveUrl

try:
    # django < 2
    from django.core.urlresolvers import reverse
except ImportError:
    # django > 2
    from django.urls import reverse


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'url': reverse,
    })
    env.add_extension(ActiveUrl)

    return env
