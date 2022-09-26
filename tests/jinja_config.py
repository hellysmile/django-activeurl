# -*- coding: utf-8 -*-
from jinja2 import Environment

from django_activeurl.ext.django_jinja import ActiveUrl
from django.urls import reverse


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'url': reverse,
    })
    env.add_extension(ActiveUrl)

    return env
