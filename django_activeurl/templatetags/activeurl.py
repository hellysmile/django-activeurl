'''activeurl django template library'''
from django import template

from classytags.core import Tag, Options
from classytags.arguments import MultiKeywordArgument

from django_activeurl import settings
from django_activeurl.utils import render_content


# django template library
register = template.Library()


class ActiveUrl(Tag):
    '''django template tag via django-classy-tags'''
    # tag name
    name = 'activeurl'

    # template tag arguments
    options = Options(
        # all key based arguments mapped to one dict
        MultiKeywordArgument('kwargs', required=False),
        blocks=[('endactiveurl', 'nodelist')]
    )

    def render_tag(self, context, kwargs, nodelist):
        '''render content with "active" urls logic'''
        # update passed arguments with default values
        for key, value in settings.ACTIVE_URL_KWARGS.items():
            kwargs.setdefault(key, value)

        # "active" html tag css class
        css_class = kwargs['css_class']
        # "active" html tag
        parent_tag = kwargs['parent_tag']
        # flipper for menu support
        menu = kwargs['menu']

        # accept from template parent_tag values such as False, None, ''
        # django 1.5 feature
        if not parent_tag:
            parent_tag = 'self'

        # get request from context
        request = context['request']

        # get full path from request
        full_path = request.get_full_path()

        # render content of template tag
        context.push()
        content = nodelist.render(context)
        context.pop()

        # check content for "active" urls
        content = render_content(
            content, full_path, parent_tag, css_class, menu
        )

        return content


# register new template tag
register.tag(ActiveUrl)
