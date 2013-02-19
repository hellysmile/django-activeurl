import sys
from hashlib import md5
from lxml.html import fromstring
from django.core.cache import cache
from django.template import Template, Context, loader
from django.test.client import RequestFactory


loader.add_to_builtins('django_activeurl.templatetags.activeurl')

requests = RequestFactory()


def render(template, context=None):
    context = Context(context)
    return Template(template).render(context)


def test_basic():
    template = '''
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
    '''

    context = {'request': requests.get('/page/')}
    html = render(template, context)

    tree = fromstring(html)
    li_elements = tree.xpath('//li')

    active_li = li_elements[0]
    assert 'class' in active_li.attrib.keys()
    css_class = active_li.attrib['class']
    assert css_class == 'active'

    inactive_li = li_elements[1]
    assert not 'class' in inactive_li.attrib.keys()


def test_already_active():
    template = '''
        {% activeurl %}
            <ul>
                <li class="active">
                    <a href="/page/">page</a>
                </li>
            </ul>
        {% endactiveurl %}
    '''

    context = {'request': requests.get('/page/')}
    html = render(template, context)

    tree = fromstring(html)
    li_elements = tree.xpath('//li')

    active_li = li_elements[0]
    assert 'class' in active_li.attrib.keys()
    css_class = active_li.attrib['class']
    assert css_class == 'active'


def test_append_css_class():
    template = '''
        {% activeurl %}
            <ul>
                <li class="link">
                    <a href="/page/">page</a>
                </li>
            </ul>
        {% endactiveurl %}
    '''

    context = {'request': requests.get('/page/')}
    html = render(template, context)

    tree = fromstring(html)
    li_elements = tree.xpath('//li')

    active_li = li_elements[0]
    assert 'class' in active_li.attrib.keys()
    css_class = active_li.attrib['class']
    assert css_class == 'link active'


def test_empty_css_class():
    template = '''
        {% activeurl %}
            <ul>
                <li class="">
                    <a href="/page/">page</a>
                </li>
            </ul>
        {% endactiveurl %}
    '''

    context = {'request': requests.get('/page/')}
    html = render(template, context)

    tree = fromstring(html)
    li_elements = tree.xpath('//li')

    active_li = li_elements[0]
    assert 'class' in active_li.attrib.keys()
    css_class = active_li.attrib['class']
    assert css_class == 'active'


def test_cache():
    html = '<ul><li><a href="/page/">page</a></li></ul>'
    template = '{% activeurl %}' + html + '{% endactiveurl %}'

    context = {'request': requests.get('/page/')}
    set_cache = render(template, context)

    if sys.version_info[0] == 3:
        data = html.encode() + b'active' + b'li' + b'/page/'
    else:
        data = html + 'active' + 'li' + '/page/'

    cache_key = 'django_activeurl.' + md5(data).hexdigest()

    assert cache.get(cache_key)


def test_submenu():
    template = '''
        {% activeurl %}
            <ul>
                <li>
                    <a href="/menu/">menu</a>
                </li>
                <li>
                    <a href="/menu/submenu/">submenu</a>
                </li>
                <li>
                    <a href="/menu/other_submenu/">other_submenu</a>
                </li>
            </ul>
        {% endactiveurl %}
    '''

    context = {'request': requests.get('/menu/submenu/')}
    html = render(template, context)

    tree = fromstring(html)
    li_elements = tree.xpath('//li')

    active_menu = li_elements[0]
    assert 'class' in active_menu.attrib.keys()
    css_class = active_menu.attrib['class']
    assert css_class == 'active'

    active_submenu = li_elements[1]
    assert 'class' in active_submenu.attrib.keys()
    css_class = active_submenu.attrib['class']
    assert css_class == 'active'

    inactive_submenu = li_elements[2]
    assert not 'class' in inactive_submenu.attrib.keys()


def test_no_parent():
    template = '''
        {% activeurl parent_tag='' %}
            <div>
                <a href="/other_page/">other_page</a>
                <hr>
                <a href="/page/">page</a>
                </li>
            </div>
        {% endactiveurl %}
    '''

    context = {'request': requests.get('/page/')}
    html = render(template, context)

    tree = fromstring(html)
    a_elements = tree.xpath('//a')

    active_a = a_elements[1]
    assert 'class' in active_a.attrib.keys()
    css_class = active_a.attrib['class']
    assert css_class == 'active'

    inactive_a = a_elements[0]
    assert not 'class' in inactive_a.attrib.keys()


def test_no_parent_submenu():
    template = '''
        {% activeurl parent_tag='' %}
            <div>
                <a href="/menu/">menu</a>
                <hr>
                <a href="/menu/submenu/">submenu</a>
                <hr>
                <a href="/menu/other_submenu/">other_submenu</a>
            </div>
        {% endactiveurl %}
    '''

    context = {'request': requests.get('/menu/submenu/')}
    html = render(template, context)

    tree = fromstring(html)
    a_elements = tree.xpath('//a')

    active_menu = a_elements[0]
    assert 'class' in active_menu.attrib.keys()
    css_class = active_menu.attrib['class']
    assert css_class == 'active'

    active_submenu = a_elements[1]
    assert 'class' in active_submenu.attrib.keys()
    css_class = active_submenu.attrib['class']
    assert css_class == 'active'

    inactive_submenu = a_elements[2]
    assert not 'class' in inactive_submenu.attrib.keys()


def test_no_parent_cache():
    html = '<div><a href="/page/">page</a></div>'
    template = '{% activeurl parent_tag='' %}' + html + '{% endactiveurl %}'

    context = {'request': requests.get('/page/')}
    set_cache = render(template, context)

    if sys.version_info[0] == 3:
        data = html.encode() + b'active' + b'' + b'/page/'
    else:
        data = html + 'active' + '' + '/page/'

    cache_key = 'django_activeurl.' + md5(data).hexdigest()

    assert cache.get(cache_key)


def test_kwargs():
    template = '''
        {% activeurl parent_tag='div' css_class='current' %}
            <div>
                <div>
                    <a href="/page/">page/</a>
                </div>
                <div>
                    <a href="/other_page/">other_page</a>
                </div>
            </div>
        {% endactiveurl %}
    '''

    context = {'request': requests.get('/page/')}
    html = render(template, context)

    tree = fromstring(html)
    div_elements = tree.xpath('//div')

    active_div = div_elements[1]
    assert 'class' in active_div.attrib.keys()
    css_class = active_div.attrib['class']
    assert css_class == 'current'

    inactive_div = div_elements[2]
    assert not 'class' in inactive_div.attrib.keys()
