'''template engine independent utils'''
import re
from hashlib import md5

from django.core.cache import cache
from django.utils.http import urlquote
from django.utils.translation import get_language
from lxml.etree import ParserError
from lxml.html import fragment_fromstring, tostring

from .conf import settings


class ImproperlyConfigured(Exception):
    '''django-like ImproperlyConfigured exception'''
    pass


class BaseRenderer(object):
    '''abstract configuration'''

    def load_configuration(self, kwargs):
        '''load configuration, merge with default settings'''
        # update passed arguments with default values
        for key, value in settings.ACTIVE_URL_KWARGS.items():
            kwargs.setdefault(key, value)

        # "active" html tag css class
        self.css_class = str(kwargs['css_class'])

        # "active" html tag*
        parent_tag = kwargs['parent_tag']
        # django > 1.5 template boolean\None variables feature
        if isinstance(parent_tag, bool):
            if not parent_tag:
                parent_tag = 'self'
            else:
                raise ImproperlyConfigured('''
                    parent_tag=True is not allowed
                ''')
        elif parent_tag is None:
            parent_tag = 'self'
        self.parent_tag = parent_tag

        # flipper for menu support
        menu = kwargs['menu']
        # django > 1.5 template boolean\None variables feature
        if isinstance(menu, bool):
            if menu:
                menu = 'yes'
            else:
                menu = 'no'
        elif menu is None:
            menu = 'no'

        # check menu configuration, set boolean value
        if menu.lower() in ('yes', 'true'):
            self.menu = True
        elif menu.lower() in ('no', 'false'):
            self.menu = False
        else:
            raise ImproperlyConfigured("Malformed Menu Value")


    def get_cache_key(self, content, full_path):
        '''generate cache key'''
        cache_key = '%s%s%s%s%s' % (
            content, self.css_class, self.parent_tag, full_path, self.menu
        )
        # fix for non ascii symbols, ensure encoding, python3 hashlib fix
        cache_key = cache_key.encode('utf-8', 'ignore')

        cache_key = md5(cache_key).hexdigest()

        cache_key = '%s.%s.%s' % (
            settings.ACTIVE_URL_CACHE_PREFIX,
            get_language(),
            cache_key
        )

        return cache_key


    def check_active(self, url, element, full_path):
        '''check "active" url, apply css_class'''
        # check missing href parameter
        if not url.attrib.get('href', None) is None:
            href = url.attrib['href'].strip()
            # cut off hashtag (anchor)
            href = re.sub(r'\#.+', '', href)
            if href == '':
                # replace href with current location
                href = full_path

            if self.menu:
                # try mark "root" (/) url as "active", in equals way
                if href == '/' == full_path:
                    is_active = True
                # skip "root" (/) url, otherwise it will be always "active"
                elif href != '/':
                    is_active = (
                        full_path.startswith(href)
                        or urlquote(full_path).startswith(href)
                        or full_path.startswith(urlquote(href))
                    )
                else:
                    is_active = False
            else:
                is_active = (
                    full_path == href
                    # maybe an urlquoted href was supplied
                    or urlquote(full_path) == href
                    or full_path == urlquote(href)
                )

            if is_active:
                # check parent tag has "class" attribute or it is empty
                if element.attrib.get('class'):
                    # prevent multiple "class" attribute adding
                    if self.css_class not in element.attrib['class']:
                        # append "active" class
                        element.attrib['class'] += ' ' + self.css_class
                else:
                    # create or set (if empty) "class" attribute
                    element.attrib['class'] = self.css_class
                return True
        # no "active" urls found
        return False


    def check_content(self, content, full_path):
        '''check content for "active" urls'''
        # valid html root tag
        try:
            # render elements tree from content
            tree = fragment_fromstring(content)
            # flag for prevent content rerendering, when no "active" urls found
            processed = False

            # if parent_tag is False\None\''\a\self
            # "active" status will be applied directly to "<a>"
            if self.parent_tag.lower() in ('a', 'self', ''):
                # xpath query to get all "<a>"
                urls = tree.xpath('.//a')
                # check "active" status for all urls
                for url in urls:
                    if self.check_active(url, url, full_path):
                        # mark flag for rerendering content
                        processed = True
            # otherwise css_class must be applied to parent_tag
            else:
                # xpath query to get all parent tags
                elements = tree.xpath('.//%s' % self.parent_tag)
                # check all elements for "active" "<a>"
                for element in elements:
                    # xpath query to get all "<a>"
                    urls = element.xpath('.//a')
                    # check "active" status for all urls
                    for url in urls:
                        if self.check_active(url, element, full_path):
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


    def render_content(self, content, full_path):
        '''check content for "active" urls, store results to django cache'''
        # try to take pre rendered content from django cache, if caching is enabled
        if settings.ACTIVE_URL_CACHE:
            cache_key = self.get_cache_key(content, full_path)

            # get cached content from django cache backend
            from_cache = cache.get(cache_key)

            # return pre rendered content if it exist in cache
            if from_cache is not None:
                return from_cache

        # render content with "active" is_active
        content = self.check_content(content, full_path)

        # write rendered content to django cache backend, if caching is enabled
        if settings.ACTIVE_URL_CACHE:
            cache.set(cache_key, content, settings.ACTIVE_URL_CACHE_TIMEOUT)

        return content
