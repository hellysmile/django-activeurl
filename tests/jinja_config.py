from __future__ import absolute_import, unicode_literals

from django_activeurl.ext.django_jinja import ActiveUrl
from django.core.urlresolvers import reverse
from jinja2 import Environment


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'url': reverse
    })
    env.add_extension(ActiveUrl)

    return env
