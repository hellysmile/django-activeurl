'''template engine independent utils'''
import re
from hashlib import md5

from lxml.html import fragment_fromstring, tostring
from lxml.etree import ParserError

from django.core.cache import cache
from django.utils.translation import get_language

from . import settings


class ImproperlyConfigured(Exception):
    '''django-like ImproperlyConfigured exception'''
    pass


def get_cache_key(content, css_class, parent_tag, full_path, menu):
    '''generate cache key'''
    cache_key = '%s%s%s%s%s' % (
        content, css_class, parent_tag, full_path, menu
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


def check_active(url, element, full_path, css_class, menu):
    '''check "active" url, apply css_class'''
    # check menu configuration, set boolean value
    if menu == 'yes':
        menu = True
    else:
        menu = False
    # check non empty href parameter
    if url.attrib.get('href'):
        # get href attribute
        href = url.attrib['href']
        # cut off hashtag (anchor)
        href = re.sub(r'\#.+', '', href)
        # compare full_path with href according to menu configuration
        if menu:
            # skip "root" (/) url, otherwise it will be always "active"
            if href != '/' or full_path == '/':
                # start with logic
                logic = full_path.startswith(href)
            else:
                logic = False
        else:
            # equals logic
            logic = full_path == href
        # "active" url found
        if logic:
            # check parent tag has "class" attribute or it is empty
            if element.attrib.get('class'):
                # prevent multiple "class" attribute adding
                if not css_class in element.attrib['class']:
                    # append "active" class
                    element.attrib['class'] += ' ' + css_class
            else:
                # create or set (if empty) "class" attribute
                element.attrib['class'] = css_class
            return True
    # no "active" urls found
    return False


def check_content(content, full_path, css_class, parent_tag, menu):
    '''check content for "active" urls'''
    # valid html root tag
    try:
        # render elements tree from content
        tree = fragment_fromstring(content)
        # flag for prevent content rerendering, when no "active" urls found
        processed = False
        # if parent_tag is False\None\''\a\self
        # "active" status will be applied directly to "<a>"
        if not parent_tag or parent_tag in ('a', 'self'):
            # xpath query to get all "<a>"
            urls = tree.xpath('.//a')
            # check "active" status for all urls
            for url in urls:
                if check_active(url, url, full_path, css_class, menu):
                    # mark flag for rerendering content
                    processed = True
        # otherwise css_class must be applied to parent_tag
        else:
            # xpath query to get all parent tags
            elements = tree.xpath('.//%s' % parent_tag)
            # check all elements for "active" "<a>"
            for element in elements:
                # xpath query to get all "<a>"
                urls = element.xpath('.//a')
                # check "active" status for all urls
                for url in urls:
                    if check_active(url, element, full_path, css_class, menu):
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


def render_content(content, full_path, parent_tag, css_class, menu):
    '''check content for "active" urls, store results to django cache'''
    if not menu in ('yes', 'no'):
        raise ImproperlyConfigured('malformed "menu" value, use "yes" or "no"')
    # try to take pre rendered content from django cache, if caching is enabled
    if settings.ACTIVE_URL_CACHE:
        cache_key = get_cache_key(
            content, css_class, parent_tag, full_path, menu
        )

        # get cached content from django cache backend
        from_cache = cache.get(cache_key)

        # return pre rendered content if it exist in cache
        if not from_cache is None:
            return from_cache

    # render content with "active" logic
    content = check_content(content, full_path, css_class, parent_tag, menu)

    # write rendered content to django cache backend, if caching is enabled
    if settings.ACTIVE_URL_CACHE:
        cache.set(cache_key, content, settings.ACTIVE_URL_CACHE_TIMEOUT)

    return content
