'''Automatic active(current/up-level) url highlighting(adding css class)
with django template tag
'''
from hashlib import md5
from lxml.html import fromstring, tostring
from django import template
from django.core.cache import cache
from classytags.core import Tag, Options
from classytags.arguments import MultiKeywordArgument
from django_activeurl import settings


register = template.Library()


class ActiveUrl(Tag):
    '''By default addition css_class is "active"
        for parent tag of all <a> which parent is <li>.
        Quick example
        {% activeurl %}
            <ul>
                <li>
                    <a href="/page/">/page/</a>
                </li>
            </ul>
        {% endactiveurl %}
        will be rendered to
            <ul>
                <li class="active">
                    <a href="/page/">page</a>
                </li>
            </ul>
        if your current request.get_full_path() starts with /page/
        starts with logic decided for applying "active" status
        for up-level <a> in your menus/submenus
    '''

    name = 'activeurl'

    # template tag arguments
    options = Options(
        MultiKeywordArgument('kwargs', required=False),
        blocks=[('endactiveurl', 'nodelist')],
    )

    def check_active(self, url, el, full_path, css_class, parent_tag):
        '''check url "active" status, apply css_class to html element'''
        # check non empty href parameter
        if url.attrib.get('href'):
            # skip "root" url
            if url.attrib['href'] != '/':
                # compare href parameter with full path
                if full_path.startswith(url.attrib['href']):
                    # check parent tag has "class" attribute
                    if el.attrib.get('class'):
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
                    return True
        return False

    def render_tag(self, context, kwargs, nodelist):
        '''renders html with "active" urls inside template tag'''
        # set attributes from kwargs
        default_kwargs = settings.DEFAULT_KWARGS
        default_kwargs.update(kwargs)
        kwargs = default_kwargs
        css_class = kwargs['css_class']
        parent_tag = kwargs['parent_tag']

        # accept from template parent_tag values such as False, None, ''
        if not parent_tag:
            parent_tag = ''

        # flag for prevent html rebuilding, when no "active" urls found
        processed = False

        # get request from context
        request = context['request']

        # get full path from request
        full_path = request.get_full_path()

        # render content inside template tag
        context.push()
        content = nodelist.render(context)
        context.pop()

        # try to take rendered html with "active" urls from cache
        if settings.CACHE_ACTIVE_URL:
            data = content + css_class + parent_tag + full_path
            data = data.encode('utf-8', 'ignore')
            cache_key = settings.CACHE_ACTIVE_URL_PREFIX \
                + md5(data).hexdigest()

            from_cache = cache.get(cache_key)
            if from_cache:
                return from_cache

        # build html tree from content inside template tag
        tree = fromstring(content)

        # if parent_tag is False\None\empty, so "active" status will be applied
        # directly to <a>
        if not parent_tag:
            # xpath query to get all <a>
            urls = tree.xpath('//a')

            # check "active" status for all urls
            for url in urls:
                if self.check_active(url, url, full_path, css_class,
                                     parent_tag):
                    processed = True

            # prevent html rebuild if no one of urls is "active"
            if processed:
                # build html from tree
                content = tostring(tree)
        # otherwise css_class must be applied to parent_tag
        else:
            # xpath query to get all parents tags
            els = tree.xpath('//%s' % parent_tag)
            for el in els:
                # xpath query to get all <a> inside current tag
                urls = el.xpath('a')
                # check "active" status for all urls
                for url in urls:
                    if self.check_active(url, el, full_path, css_class,
                                         parent_tag):
                        # flag for rebuild html tree
                        processed = True
                        # stop check other <a> inside current parent_tag
                        break

            # do not rebuild html if no "active" urls inside parent_tag
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
