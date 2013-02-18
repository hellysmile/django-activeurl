from django.conf.urls import patterns, include, url
from django.contrib import admin
from example.views import IndexTemplateView


admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'example.views.home', name='home'),
    # url(r'^example/', include('example.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^simplepage/', include('simplepage.urls')),

    url(r'^$', IndexTemplateView.as_view(), name='index'),
)
