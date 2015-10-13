'''template engine independent utils'''
from __future__ import absolute_import, unicode_literals

import re
from hashlib import md5

from django.core.cache import cache
from django.utils.http import urlquote
from django.utils.translation import get_language
from lxml.etree import ParserError
from lxml.html import fragment_fromstring, tostring

from .__init__ import __version__
from .conf import settings


class ImproperlyConfigured(Exception):
    '''django-like ImproperlyConfigured exception'''
    pass


class Configuration(object):
    '''abstract configuration'''

    def load_configuration(self, **kwargs):
        '''load configuration, merge with default settings'''
        # update passed arguments with default values
        for key in settings.ACTIVE_URL_KWARGS:
            kwargs.setdefault(key, settings.ACTIVE_URL_KWARGS[key])

        # "active" html tag css class
        self.css_class = kwargs['css_class']
        # "active" html tag
        self.parent_tag = kwargs['parent_tag']
        # flipper for menu support
        self.menu = kwargs['menu']


def get_cache_key(content, **kwargs):
    '''generate cache key'''
    cache_key = ''
    for key in sorted(kwargs.keys()):
        cache_key = '{cache_key}.{key}:{value}'.format(
            cache_key=cache_key,
            key=key,
            value=kwargs[key]
        )

    cache_key = '{content}{cache_key}'.format(
        content=content,
        cache_key=cache_key
    )

    # fix for non ascii symbols, ensure encoding, python3 hashlib fix
    cache_key = cache_key.encode('utf-8', 'ignore')
    cache_key = md5(cache_key).hexdigest()

    cache_key = '{prefix}.{version}.{language}.{cache_key}'.format(
        prefix=settings.ACTIVE_URL_CACHE_PREFIX,
        version=__version__,
        language=get_language(),
        cache_key=cache_key
    )

    return cache_key


def check_active(url, element, **kwargs):
    '''check "active" url, apply css_class'''
    # django > 1.5 template boolean\None variables feature
    if isinstance(kwargs['menu'], bool):
        if kwargs['menu']:
            kwargs['menu'] = 'yes'
        else:
            kwargs['menu'] = 'no'
    elif kwargs['menu'] is None:
        kwargs['menu'] = 'no'
    # check menu configuration, set boolean value
    if kwargs['menu'].lower() in ('yes', 'true'):
        kwargs['menu'] = True
    elif kwargs['menu'].lower() in ('no', 'false'):
        kwargs['menu'] = False
    else:
        raise ImproperlyConfigured('''
            malformed menu value
        ''')
    # check missing href parameter
    if not url.attrib.get('href', None) is None:
        # get href attribute
        href = url.attrib['href'].strip()
        # cut off hashtag (anchor)
        href = re.sub(r'\#.+', '', href)
        # check empty href
        if href == '':
            # replace href with current location
            href = kwargs['full_path']
        # compare full_path with href according to menu configuration

        if kwargs['menu']:
            # try mark "root" (/) url as "active", in equals way
            if href == '/' == kwargs['full_path']:
                logic = True
            # skip "root" (/) url, otherwise it will be always "active"
            elif href != '/':
                # start with logic
                logic = (
                    kwargs['full_path'].startswith(href)
                    or
                    # maybe an urlquoted href was supplied
                    urlquote(kwargs['full_path']).startswith(href)
                    or
                    kwargs['full_path'].startswith(urlquote(href))
                )
            else:
                logic = False
        else:
            # equals logic
            logic = (
                kwargs['full_path'] == href
                or
                # maybe an urlquoted href was supplied
                urlquote(kwargs['full_path']) == href
                or
                kwargs['full_path'] == urlquote(href)
            )
        # "active" url found
        if logic:
            # check parent tag has "class" attribute or it is empty
            if element.attrib.get('class'):
                # prevent multiple "class" attribute adding
                if kwargs['css_class'] not in element.attrib['class']:
                    # append "active" class
                    element.attrib['class'] += ' {css_class}'.format(
                        css_class=kwargs['css_class']
                    )
            else:
                # create or set (if empty) "class" attribute
                element.attrib['class'] = kwargs['css_class']
            return True
    # no "active" urls found
    return False


def check_content(content, **kwargs):
    '''check content for "active" urls'''
    # valid html root tag
    try:
        # render elements tree from content
        tree = fragment_fromstring(content)
        # flag for prevent content rerendering, when no "active" urls found
        processed = False
        # django > 1.5 template boolean\None variables feature
        if isinstance(kwargs['parent_tag'], bool):
            if not kwargs['parent_tag']:
                kwargs['parent_tag'] = 'self'
            else:
                raise ImproperlyConfigured('''
                    parent_tag=True is not allowed
                ''')
        elif kwargs['parent_tag'] is None:
            kwargs['parent_tag'] = 'self'
        # if parent_tag is False\None\''\a\self
        # "active" status will be applied directly to "<a>"
        if kwargs['parent_tag'].lower() in ('a', 'self', ''):
            # xpath query to get all "<a>"
            urls = tree.xpath('.//a')
            # check "active" status for all urls
            for url in urls:
                if check_active(url, url, **kwargs):
                    # mark flag for rerendering content
                    processed = True
        # otherwise css_class must be applied to parent_tag
        else:
            # xpath query to get all parent tags
            elements = tree.xpath('.//{parent_tag}'.format(
                parent_tag=kwargs['parent_tag']
            ))
            # check all elements for "active" "<a>"
            for element in elements:
                # xpath query to get all "<a>"
                urls = element.xpath('.//a')
                # check "active" status for all urls
                for url in urls:
                    if check_active(url, element, **kwargs):
                        # flag for rerendering content tree
                        processed = True
                        # stop checking other "<a>"
                        break
        # do not rerender content if no "active" urls found
        if processed:
            # render content from tree
            return tostring(tree, encoding='unicode')
    # not valid html root tag
    except ParserError:
        # raise an exception with configuration example
        raise ImproperlyConfigured('''
            content of {% activeurl %} must have valid html root tag
            for example
                {% activeurl %}
                    <ul>
                        <li>
                            <a href="/page/">page</a>
                        </li>
                        <li>
                            <a href="/other_page/">other_page</a>
                        </li>
                    </ul>
                {% endactiveurl %}
            in this case <ul> is valid content root tag
        ''')
    return content


def render_content(content, **kwargs):
    '''check content for "active" urls, store results to django cache'''
    # try to take pre rendered content from django cache, if caching is enabled
    if settings.ACTIVE_URL_CACHE:
        cache_key = get_cache_key(content, **kwargs)

        # get cached content from django cache backend
        from_cache = cache.get(cache_key)

        # return pre rendered content if it exist in cache
        if from_cache is not None:
            return from_cache

    # render content with "active" logic
    content = check_content(content, **kwargs)

    # write rendered content to django cache backend, if caching is enabled
    if settings.ACTIVE_URL_CACHE:
        cache.set(cache_key, content, settings.ACTIVE_URL_CACHE_TIMEOUT)

    return content
