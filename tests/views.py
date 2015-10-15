from django.http import HttpResponse
from django.shortcuts import render


def dummy_view(request):
    return HttpResponse()


def djnago_template_view(request):
    return render(request, 'django.html', {})


def jinja_template_view(request):
    return render(request, 'jinja.html', {})
