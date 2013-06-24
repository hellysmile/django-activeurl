'''jinja extenions for django_jinja/coffin/jingo'''
from jinja2 import nodes
from jinja2.ext import Extension

from django_activeurl import settings
from django_activeurl.utils import render_content


class ActiveUrl(Extension):
    '''activeurl jinja extension for django_jinja/coffin/jingo'''

    # a set of names that trigger the extension.
    tags = set(['activeurl'])

    def parse(self, parser):
        '''parse content of extension'''
        # line number of token that started the tag.
        lineno = next(parser.stream).lineno

        # get single options argument
        kwargs = [parser.parse_expression()]

        # parse content of the activeurl block up to endactiveurl
        body = parser.parse_statements(['name:endactiveurl'], drop_needle=True)

        return nodes.CallBlock(
            self.call_method('render_tag', kwargs), [], [], body
        ).set_lineno(lineno)

    def render_tag(self, kwargs, caller):
        '''render content with "active" urls logic'''
        # render content of extension
        content = caller()

        # update passed arguments with default values
        for key, value in settings.ACTIVE_URL_KWARGS.items():
            kwargs.setdefault(key, value)

        # "active" html tag css class
        css_class = kwargs['css_class']
        # "active" html tag
        parent_tag = kwargs['parent_tag']
        # flipper for menu support
        menu = kwargs['menu']
        # full path passed from request via global options function
        full_path = kwargs['full_path']

        # accept from template parent_tag values such as False, None, ''
        if not parent_tag:
            parent_tag = 'self'

        # check content for "active" urls
        content = render_content(
            content, full_path, parent_tag, css_class, menu
        )
        return content
