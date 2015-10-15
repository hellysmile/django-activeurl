# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

try:
    from django.conf.urls.defaults import patterns, url
except ImportError:
    from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    '',
    url(r'^$', views.dummy_view),
    url(r'^page/$', views.dummy_view),
    url(r'^menu/$', views.dummy_view),
    url(r'^menu/submenu/$', views.dummy_view),
    url(r'^страница/$', views.dummy_view),
    url(r'^другая_страница/$', views.dummy_view, name='non-ascii-reverse'),
    url(r'^template/django/$', views.djnago_template_view),
    url(r'^template/jinja/$', views.jinja_template_view),
)
