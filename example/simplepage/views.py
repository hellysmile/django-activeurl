from django.views.generic import ListView, DetailView
from simplepage.models import SimplePage


class NaviMixin(object):
    def get_context_data(self, **kwargs):
        context = super(NaviMixin, self).get_context_data(**kwargs)
        context['navi_simplepages'] = \
            SimplePage.objects.all().defer('content')
        return context


class SimplePageListView(NaviMixin, ListView):
    template_name = 'simplepage/list.html'
    model = SimplePage


class SimplePageDetailView(NaviMixin, DetailView):
    template_name = 'simplepage/detail.html'
    model = SimplePage
    slug_field = 'slug'
