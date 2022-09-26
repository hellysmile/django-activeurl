# -*- coding: utf-8 -*-
"""activeurl django template library"""
from classytags.arguments import MultiKeywordArgument
from classytags.core import Options, Tag
from django import template

from django_activeurl.utils import Configuration, render_content

# django template library
register = template.Library()


@register.tag(name='activeurl')
class ActiveUrl(Tag, Configuration):
    """django template tag via django-classy-tags"""

    # template tag arguments
    options = Options(
        # all key based arguments mapped to one dict
        MultiKeywordArgument('kwargs', required=False),
        blocks=[('endactiveurl', 'nodelist')],
    )

    def render_tag(self, context, kwargs, nodelist):
        """render content with "active" urls logic"""
        # load configuration from passed options
        self.load_configuration(**kwargs)

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
            content,
            full_path=self.full_path,
            parent_tag=self.parent_tag,
            css_class=self.css_class,
            menu=self.menu,
            ignore_params=self.ignore_params,
        )

        return content
