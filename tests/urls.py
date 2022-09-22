# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import re_path


def view(request):
    return HttpResponse()


def djnago_template_view(request):
    return render(request, 'django.html', {})


def jinja_template_view(request):
    return render(request, 'jinja.html', {})


urlpatterns = [
    re_path(r'^$', view),
    re_path(r'^template/django/$', djnago_template_view),
    re_path(r'^template/jinja/$', jinja_template_view),
    re_path(r'^page/$', view),
    re_path(r'^menu/$', view),
    re_path(r'^menu/submenu/$', view),
    re_path(r'^страница/$', view),
    re_path(r'^другая_страница/$', view, name='non-ascii-reverse'),
]
