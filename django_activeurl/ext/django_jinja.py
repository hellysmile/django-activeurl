'''jinja extenions for django_jinja/coffin/jingo'''
from jinja2 import nodes
from jinja2.ext import Extension

from ..utils import render_content, Configuration


class ActiveUrl(Extension, Configuration):
    '''activeurl jinja extension for django_jinja/coffin/jingo'''

    # a set of names that trigger the extension.
    tags = set(['activeurl'])

    def parse(self, parser):
        '''parse content of extension'''
        # line number of token that started the tag
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

        # load configuration from passed options
        self.load_configuration(kwargs)

        # full path passed from request via global options function
        self.full_path = kwargs['full_path']

        # check content for "active" urls
        content = render_content(
            content, self.full_path, self.parent_tag, self.css_class, self.menu
        )
        return content
