from django.core.urlresolvers import reverse
from django_activeurl.ext.django_jinja import ActiveUrl
from django_activeurl.ext.utils import options as activeurl_options
from jinja2 import Environment


def environment(**options):
    options['extensions'] = [ActiveUrl]
    env = Environment(**options)
    env.globals.update({
        'url': reverse,
        'options': activeurl_options
    })
    return env
