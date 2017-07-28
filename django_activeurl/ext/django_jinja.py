# -*- coding: utf-8 -*-
'''jinja extenions for django_jinja/django 1.8+'''
from __future__ import absolute_import, unicode_literals

from jinja2 import lexer, nodes
from jinja2.ext import Extension

from ..utils import Configuration, render_content


class ActiveUrl(Extension, Configuration):
    '''activeurl jinja extension for django_jinja/coffin/jingo'''

    # a set of names that trigger the extension.
    tags = {'activeurl'}

    def parse(self, parser):
        '''parse content of extension'''
        # line number of token that started the tag
        lineno = next(parser.stream).lineno

        # template context
        context = nodes.ContextReference()

        # parse keyword arguments
        kwargs = []

        while parser.stream.look().type == lexer.TOKEN_ASSIGN:
            key = parser.stream.expect(lexer.TOKEN_NAME)
            next(parser.stream)
            kwargs.append(
                nodes.Keyword(key.value, parser.parse_expression()),
            )
            parser.stream.skip_if('comma')
        # parse content of the activeurl block up to endactiveurl
        body = parser.parse_statements(['name:endactiveurl'], drop_needle=True)

        args = [context]

        call_method = self.call_method(
            'render_tag',
            args=args,
            kwargs=kwargs,
        )

        return nodes.CallBlock(call_method, [], [], body).set_lineno(lineno)

    def render_tag(self, context, caller, **kwargs):
        '''render content with "active" urls logic'''
        # load configuration from passed options
        self.load_configuration(**kwargs)

        # get request from context
        request = context['request']

        # get full path from request
        self.full_path = request.get_full_path()

        # render content of extension
        content = caller()

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
