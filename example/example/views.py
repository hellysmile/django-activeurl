from django.views.generic import TemplateView
from simplepage.views import NaviMixin


class IndexTemplateView(NaviMixin, TemplateView):
    template_name = 'skel/index.html'
