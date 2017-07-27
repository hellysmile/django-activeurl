'''template engine independent utils'''
from hashlib import md5

from django.core.cache import cache
from django.utils.http import urlquote
from django.utils.six.moves.urllib import parse as urlparse
from django.utils.translation import get_language
from lxml.etree import ParserError
from lxml.html import fragment_fromstring, tostring

from .conf import settings


class ImproperlyConfigured(Exception):
    '''django-like ImproperlyConfigured exception'''
    pass


class Configuration(object):
    '''abstract configuration'''

    def load_configuration(self, kwargs):
        '''load configuration, merge with default settings'''
        # update passed arguments with default values
        for key, value in settings.ACTIVE_URL_KWARGS.items():
            kwargs.setdefault(key, value)

        # "active" html tag css class
        self.css_class = str(kwargs['css_class'])
        # "active" html tag
        self.parent_tag = kwargs['parent_tag']
        # flipper for menu support
        self.menu = kwargs['menu']
        # whether to ignore / chomp get_params
        self.ignore_params = kwargs['ignore_params']


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


def yesno_to_bool(value, varname):
    """Return True/False from "yes"/"no".

    :param value: template keyword argument value
    :type value: string
    :param varname: name of the variable, for use on exception raising
    :type varname: string
    :raises: :exc:`ImproperlyConfigured`

    Django > 1.5 template boolean/None variables feature.
    """
    if isinstance(value, bool):
        if value:
            value = 'yes'
        else:
            value = 'no'
    elif value is None:
        value = 'no'

    # check value configuration, set boolean value
    if value.lower() in ('yes', 'true'):
        value = True
    elif value.lower() in ('no', 'false'):
        value = False
    else:
        raise ImproperlyConfigured(
            'activeurl: malformed param value for %s' % varname
        )
    return value


def check_active(url, element, full_path, css_class, menu, ignore_params):
    '''check "active" url, apply css_class'''
    menu = yesno_to_bool(menu, 'menu')
    ignore_params = yesno_to_bool(ignore_params, 'ignore_params')

    # check missing href parameter
    if not url.attrib.get('href', None) is None:
        # get href attribute
        href = url.attrib['href'].strip()

        # split into urlparse object
        href = urlparse.urlsplit(href)

        # cut off hashtag (anchor)
        href = href._replace(fragment='')

        # cut off get params (?key=var&etc=var2)
        if ignore_params:
            href = href._replace(query='')

        # build urlparse object back into string
        href = urlparse.urlunsplit(href)

        # check empty href
        if href == '':
            # replace href with current location
            href = full_path
        # compare full_path with href according to menu configuration

        if menu:
            # try mark "root" (/) url as "active", in equals way
            if href == '/' == full_path:
                logic = True
            # skip "root" (/) url, otherwise it will be always "active"
            elif href != '/':
                # start with logic
                logic = (
                    full_path.startswith(href)
                    or
                    # maybe an urlquoted href was supplied
                    urlquote(full_path).startswith(href)
                    or
                    full_path.startswith(urlquote(href))
                )
            else:
                logic = False
        else:
            # equals logic
            logic = (
                full_path == href
                or
                # maybe an urlquoted href was supplied
                urlquote(full_path) == href
                or
                full_path == urlquote(href)
            )
        # "active" url found
        if logic:
            # check parent tag has "class" attribute or it is empty
            if element.attrib.get('class'):
                # prevent multiple "class" attribute adding
                if css_class not in element.attrib['class']:
                    # append "active" class
                    element.attrib['class'] += ' ' + css_class
            else:
                # create or set (if empty) "class" attribute
                element.attrib['class'] = css_class
            return True
    # no "active" urls found
    return False


def check_content(
    content, full_path, css_class, parent_tag, menu, ignore_params
):
    '''check content for "active" urls'''
    # valid html root tag
    try:
        # render elements tree from content
        tree = fragment_fromstring(content)
        # flag for prevent content rerendering, when no "active" urls found
        processed = False
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
        # if parent_tag is False\None\''\a\self
        # "active" status will be applied directly to "<a>"
        if parent_tag.lower() in ('a', 'self', ''):
            # xpath query to get all "<a>"
            urls = tree.xpath('.//a')
            # check "active" status for all urls
            for url in urls:
                if check_active(
                    url, url, full_path, css_class, menu, ignore_params
                ):
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
                    if check_active(
                        url, element, full_path, css_class, menu, ignore_params
                    ):
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


def render_content(
    content, full_path, parent_tag, css_class, menu, ignore_params
):
    '''check content for "active" urls, store results to django cache'''
    # try to take pre rendered content from django cache, if caching is enabled
    if settings.ACTIVE_URL_CACHE:
        cache_key = get_cache_key(
            content, css_class, parent_tag, full_path, menu
        )

        # get cached content from django cache backend
        from_cache = cache.get(cache_key)

        # return pre rendered content if it exist in cache
        if from_cache is not None:
            return from_cache

    # render content with "active" logic
    content = check_content(
        content, full_path, css_class, parent_tag, menu, ignore_params
    )

    # write rendered content to django cache backend, if caching is enabled
    if settings.ACTIVE_URL_CACHE:
        cache.set(cache_key, content, settings.ACTIVE_URL_CACHE_TIMEOUT)

    return content
