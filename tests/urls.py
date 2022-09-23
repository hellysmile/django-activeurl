# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import path


def view(request):
    return HttpResponse()


def django_template_view(request):
    return render(request, 'django.html', {})


def jinja_template_view(request):
    return render(request, 'jinja.html', {})


urlpatterns = [
    path('', view),
    path('template/django/', django_template_view),
    path('template/jinja/', jinja_template_view),
    path('page/', view),
    path('menu/', view),
    path('menu/submenu/', view),
    path('страница/', view),
    path('другая_страница/', view, name='non-ascii-reverse'),
]
