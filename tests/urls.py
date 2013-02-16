from django.conf.urls import patterns, url
from django.http import HttpResponse


def response(request):
    return HttpResponse()


urlpatterns = patterns('',
    url(r'^page/$', response),
    url(r'^menu/submenu/$', response),
)
