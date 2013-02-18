'''Automatic active(current/up-level) url highlighting(adding css class)
with django template tag
'''
import sys
from lxml.html import fromstring, tostring
from django import template
from django.core.cache import cache
try:
    from hashlib import md5 as md5_constructor
except ImportError:
    from django.utils.hashcompat import md5_constructor
from classytags.core import Tag, Options
from classytags.arguments import MultiKeywordArgument
from django_activeurl import settings


register = template.Library()


class ActiveUrl(Tag):
    '''By default additional css class is "active"
        for parent tag of all <a> which parent is <li>.
        Quick example
        {% activeurl %}
            <ul>
                <li>
                    <a href="/page/">/page/</a>
                </li>
            </ul>
        {% endactiveurl %}
        will be rendered into
            <ul>
                <li class="active">
                    <a href="/page/">page</a>
                </li>
            </ul>
        if request.get_full_path() starts with /page/
        starts with logic decided to apply "active" status
        for up-level urls from current url.
    '''

    name = 'activeurl'

    # template tag arguments
    options = Options(
        MultiKeywordArgument('kwargs', required=False),
        blocks=[('endactiveurl', 'nodelist')],
    )

    def render_tag(self, context, kwargs, nodelist):
        '''renders html with "active" urls inside template tag'''
        # set attributes from kwargs
        default_kwargs = settings.DEFAULT_KWARGS
        default_kwargs.update(kwargs)
        kwargs = default_kwargs
        css_class = kwargs['css_class']
        parent_tag = kwargs['parent_tag']

        # flag for preventing rendering, when no "active" urls found
        processed = False

        # get request from context
        request = context['request']

        # get full path from request
        full_path = request.get_full_path()

        # render content inside template tag
        context.push()
        content = nodelist.render(context)

        # try to take rendered html with "active" urls from cache
        if settings.CACHE_ACTIVE_URL:
            if sys.version_info >= (3, ):
                data = content.encode() + css_class.encode() + \
                    parent_tag.encode() + full_path.encode()
            else:
                data = content + css_class + parent_tag + full_path

            cache_key = settings.CACHE_ACTIVE_URL_PREFIX \
                + md5_constructor(data).hexdigest()

            from_cache = cache.get(cache_key)
            if from_cache:
                return from_cache

        # build tree from content inside template tag
        tree = fromstring(content)

        # xpath query to get all parents tags
        els = tree.xpath('//%s' % parent_tag)
        for el in els:
            # xpath query to get all <a> inside current tag
            urls = el.xpath('a')
            for url in urls:
                # check non empty href parameter
                if 'href' in url.attrib.keys():
                    # skip "root" url
                    if url.attrib['href'] != '/':
                        # compare href parameter with full path
                        if full_path.startswith(url.attrib['href']):
                            # check parent tag has "class" attribute
                            if 'class' in el.attrib.keys():
                                # prevent multiple "class" adding
                                if not css_class in el.attrib['class']:
                                    # check for empty "class" attribute
                                    if el.attrib['class']:
                                        # append "active" class
                                        el.attrib['class'] += ' ' + css_class
                                    else:
                                        # set "class" attribute
                                        el.attrib['class'] = css_class
                            else:
                                # create "class" attribute
                                el.attrib['class'] = css_class
                            # flag for rendering tree
                            processed = True
                            # stop checking other <a> inside current parent_tag
                            break

        context.pop()

        # checking status of founding "active" url
        if processed:
            # build html from tree
            content = tostring(tree)

            # write rendered html to cache, if caching is enabled
            if settings.CACHE_ACTIVE_URL:
                cache.set(cache_key, content,
                          settings.CACHE_ACTIVE_URL_TIMEOUT)

        return content

# register new template tag
register.tag(ActiveUrl)
