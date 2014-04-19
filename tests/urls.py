# -*- coding: utf-8 -*-
from __future__ import unicode_literals

try:
    from django.conf.urls.defaults import patterns, url
except ImportError:
    from django.conf.urls import patterns, url
from django.http import HttpResponse


def view(request):
    return HttpResponse()


urlpatterns = patterns(
    '',
    url(r'^$', view),
    url(r'^page/$', view),
    url(r'^menu/$', view),
    url(r'^menu/submenu/$', view),
    url(r'^страница/$', view),
    url(r'^другая_страница/$', view, name='non-ascii-reverse')
)
