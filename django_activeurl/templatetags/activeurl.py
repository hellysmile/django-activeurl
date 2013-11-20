'''activeurl django template library'''
from django import template
from classytags.core import Tag, Options
from classytags.arguments import MultiKeywordArgument

from ..utils import render_content, Configuration


# django template library
register = template.Library()


class ActiveUrl(Tag, Configuration):
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

        # load configuration from passed options
        self.load_configuration(kwargs)

        # get request from context
        request = context['request']

        # get full path from request
        self.full_path = request.get_full_path()

        # render content of template tag
        context.push()
        content = nodelist.render(context)
        context.pop()

        # check content for "active" urls
        content = render_content(
            content, self.full_path, self.parent_tag, self.css_class, self.menu
        )

        return content


# register new template tag
register.tag(ActiveUrl)
