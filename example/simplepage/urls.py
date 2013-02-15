from django.conf.urls import patterns, url
from simplepage.views import SimplePageListView, SimplePageDetailView


urlpatterns = patterns('',
    url(r'^$', SimplePageListView.as_view(), name='simplepages_list'),
    url(r'^(?P<slug>[-\w]+?)/$', SimplePageDetailView.as_view(), name='simplepage_detail'),
)
