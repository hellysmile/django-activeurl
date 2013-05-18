# -*- coding: utf-8 -*-
from hashlib import md5
from lxml.html import fragment_fromstring, fromstring
from django.core.cache import cache
from django.template import Template, Context, loader
from django.test.client import RequestFactory
from django_activeurl.utils import ImproperlyConfigured


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

    tree = fragment_fromstring(html)
    li_elements = tree.xpath('//li')

    active_li = li_elements[0]

    assert active_li.attrib.get('class')
    assert 'active' == active_li.attrib['class']

    inactive_li = li_elements[1]

    assert not inactive_li.attrib.get('class')


def test_no_active():
    template = '''
        {% activeurl %}
            <ul>
                <li>
                    <a href="/other_page/">other_page</a>
                </li>
            </ul>
        {% endactiveurl %}
    '''

    context = {'request': requests.get('/page/')}
    html = render(template, context)

    tree = fragment_fromstring(html)
    li_elements = tree.xpath('//li')

    inactive_li = li_elements[0]

    assert not inactive_li.attrib.get('class')


def test_non_ascii():
    template = '''
        {% activeurl %}
            <ul>
                <li>
                    <a href="/страница/">страница</a>
                </li>
                <li>
                    <a href="/другая_страница/">другая_страница</a>
                </li>
            </ul>
        {% endactiveurl %}
    '''

    context = {'request': requests.get('/страница/')}
    html = render(template, context)

    tree = fragment_fromstring(html)
    li_elements = tree.xpath('//li')

    active_li = li_elements[0]

    assert active_li.attrib.get('class')
    assert 'active' == active_li.attrib['class']

    inactive_li = li_elements[1]

    assert not inactive_li.attrib.get('class')


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

    tree = fragment_fromstring(html)
    li_elements = tree.xpath('//li')

    active_li = li_elements[0]

    assert active_li.attrib.get('class')
    assert 'active' == active_li.attrib['class']


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

    tree = fragment_fromstring(html)
    li_elements = tree.xpath('//li')

    active_li = li_elements[0]

    assert active_li.attrib.get('class')
    assert 'link active' == active_li.attrib['class']


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

    tree = fragment_fromstring(html)
    li_elements = tree.xpath('//li')

    active_li = li_elements[0]

    assert active_li.attrib.get('class')
    assert 'active' == active_li.attrib['class']


def test_cache():
    html = '<ul><li><a href="/page/">page</a></li></ul>'
    template = '{% activeurl %}' + html + '{% endactiveurl %}'

    context = {'request': requests.get('/page/')}
    set_cache = render(template, context)

    data = html + 'active' + 'li' + '/page/'
    data = data.encode()

    cache_key = 'django_activeurl.' + md5(data).hexdigest()

    from_cache = cache.get(cache_key)

    assert from_cache

    from_cache = from_cache.decode()

    get_cache = render(template, context)

    assert from_cache == set_cache == get_cache


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

    tree = fragment_fromstring(html)
    li_elements = tree.xpath('//li')

    active_menu = li_elements[0]

    assert active_menu.attrib.get('class')
    assert 'active' == active_menu.attrib['class']

    active_submenu = li_elements[1]

    assert active_submenu.attrib.get('class')
    assert 'active' == active_submenu.attrib['class']

    inactive_submenu = li_elements[2]

    assert not inactive_submenu.attrib.get('class')


def test_no_parent():
    template = '''
        {% activeurl parent_tag='' %}
            <div>
                <a href="/page/">page</a>
            </div>
        {% endactiveurl %}
        {% activeurl parent_tag='a' %}
            <div>
                <a href="/page/">page</a>
            </div>
        {% endactiveurl %}
        {% activeurl parent_tag='self' %}
            <div>
                <a href="/page/">page</a>
                <hr>
                <a href="/other_page/">other_page</a>
            </div>
        {% endactiveurl %}
    '''

    context = {'request': requests.get('/page/')}
    html = render(template, context)

    tree = fromstring(html)
    a_elements = tree.xpath('//a')

    active_a = a_elements[:-1]

    for a in active_a:
        assert a.attrib.get('class')
        assert 'active' == a.attrib['class']

    inactive_a = a_elements[-1]

    assert not inactive_a.attrib.get('class')


def test_no_parent_submenu():
    template = '''
        {% activeurl parent_tag='self' %}
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

    tree = fragment_fromstring(html)
    a_elements = tree.xpath('//a')

    active_menu = a_elements[0]

    assert active_menu.attrib.get('class')
    assert 'active' == active_menu.attrib['class']

    active_submenu = a_elements[1]

    assert active_submenu.attrib.get('class')
    assert 'active' == active_submenu.attrib['class']

    inactive_submenu = a_elements[2]

    assert not inactive_submenu.attrib.get('class')


def test_no_parent_cache():
    html = '<div><a href="/page/">page</a></div>'
    template = '{% activeurl parent_tag="self" %}' + html \
        + '{% endactiveurl %}'

    context = {'request': requests.get('/page/')}
    set_cache = render(template, context)

    data = html + 'active' + 'self' + '/page/'
    data = data.encode()

    cache_key = 'django_activeurl.' + md5(data).hexdigest()

    from_cache = cache.get(cache_key)

    assert from_cache

    from_cache = from_cache.decode()

    get_cache = render(template, context)

    assert from_cache == set_cache == get_cache


def test_kwargs():
    template = '''
        {% activeurl parent_tag='div' css_class='current' %}
            <div>
                <div>
                    <a href="/other_page/">other_page</a>
                </div>
                <div>
                    <a href="/page/">page</a>
                </div>
            </div>
        {% endactiveurl %}
    '''

    context = {'request': requests.get('/page/')}
    html = render(template, context)

    tree = fragment_fromstring(html)
    div_elements = tree.xpath('//div')

    active_div = div_elements[-1]

    assert active_div.attrib.get('class')
    assert 'current' == active_div.attrib['class']

    for inactive_div in div_elements[:-1]:
        assert not inactive_div.attrib.get('class')


def test_kwargs_multiple_urls():
    template = '''
        {% activeurl parent_tag='p' css_class='highlight' %}
            <div>
                <p>
                    <a href="/other_page/">other_page</a>
                </p>
                <p>
                    <a href="/page/">page</a>
                    <br>
                    <a href="/other_page/">other_page</a>
                </p>
            </div>
        {% endactiveurl %}
    '''

    context = {'request': requests.get('/page/')}
    html = render(template, context)

    tree = fragment_fromstring(html)
    p_elements = tree.xpath('//p')

    active_p = p_elements[1]

    assert active_p.attrib.get('class')
    assert 'highlight' == active_p.attrib['class']

    inactive_p = p_elements[0]

    assert not inactive_p.attrib.get('class')


def test_kwargs_multiple_urls_nested_tags():
    template = '''
        {% activeurl parent_tag='tr' css_class='active_row'%}
            <div>
                <table>
                    <tr>
                        <td>
                            <a href="/page/">page</a>
                        </td>
                        <td>
                            <a href="/other_page/">other_page</a>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <a href="/other_page/">other_page</a>
                        </td>
                    </tr>
                </table>
            </div>
        {% endactiveurl %}
    '''

    context = {'request': requests.get('/page/')}
    html = render(template, context)

    tree = fragment_fromstring(html)

    tr_elements = tree.xpath('//tr')

    active_tr = tr_elements[0]

    assert active_tr.attrib.get('class')
    assert 'active_row' == active_tr.attrib['class']

    inactive_tr = tr_elements[1]

    assert not inactive_tr.attrib.get('class')


def test_no_valid_html_root_tag():
    template = '''
            <ul>
                {% activeurl %}
                    <li>
                        <a href="/page/">page</a>
                    </li>
                    <li>
                        <a href="/other_page/">other_page</a>
                    </li>
                {% endactiveurl %}
            </ul>
    '''

    context = {'request': requests.get('/page/')}
    try:
        render(template, context)
        assert False
    except ImproperlyConfigured:
        pass
