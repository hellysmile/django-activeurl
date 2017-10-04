# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from hashlib import md5

from django.core.cache import cache
from django.template import Context, Template
from django.test.client import Client, RequestFactory
from django.utils.translation import get_language
from django_activeurl import __version__
from django_activeurl.conf import settings
from django_activeurl.utils import ImproperlyConfigured
from lxml.html import fragment_fromstring, fromstring

try:
    # django >= 1.7
    from django.template.base import add_to_builtins
except ImportError:
    # django >= 1.9
    def add_to_builtins(module):
        from django.template.engine import Engine
        template_engine = Engine.get_default()
        template_engine.builtins.append(module)
        template_engine.template_builtins = \
            template_engine.get_template_builtins(template_engine.builtins)

add_to_builtins('django_activeurl.templatetags.activeurl')

requests = RequestFactory()
client = Client()


def render(template, context=None):
    context = Context(context)
    return Template(template).render(context)


def get_cache_params(url, **kwargs):
    for key in settings.ACTIVE_URL_KWARGS:
        kwargs.setdefault(key, settings.ACTIVE_URL_KWARGS[key])

    kwargs['full_path'] = url

    cache_key = ''
    for key in sorted(kwargs.keys()):
        cache_key = '{cache_key}.{key}:{value}'.format(
            cache_key=cache_key,
            key=key,
            value=kwargs[key],
        )

    return cache_key


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

    assert active_li.attrib.get('class', False)
    assert 'active' == active_li.attrib['class']

    inactive_li = li_elements[1]

    assert not inactive_li.attrib.get('class', False)


def test_hashtag():
    template = '''
        {% activeurl %}
            <ul>
                <li>
                    <a href="/page/#hashtag">page</a>
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

    assert active_li.attrib.get('class', False)
    assert 'active' == active_li.attrib['class']

    inactive_li = li_elements[1]

    assert not inactive_li.attrib.get('class', False)


def test_ignore_params():
    template = '''
        {% activeurl ignore_params='yes' %}
            <ul>
                <li>
                    <a href="/page/?heyworld=moo">page</a>
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

    assert active_li.attrib.get('class', False)
    assert 'active' == active_li.attrib['class']

    inactive_li = li_elements[1]

    assert not inactive_li.attrib.get('class', False)
    
    
def test_ignore_params_with_no_menu():
    template = '''
        {% activeurl menu="no" ignore_params='yes' %}
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

    context = {'request': requests.get('/page/?foo=bar&bar=foo')}
    html = render(template, context)

    tree = fragment_fromstring(html)
    li_elements = tree.xpath('//li')

    active_li = li_elements[0]

    assert active_li.attrib.get('class', False)
    assert 'active' == active_li.attrib['class']

    inactive_li = li_elements[1]

    assert not inactive_li.attrib.get('class', False)


def test_disabled_menu_root_path():
    template = '''
        {% activeurl menu='no' %}
            <ul>
                <li>
                    <a href="/">root</a>
                </li>
                <li>
                    <a href="/other_page/">other_page</a>
                </li>
            </ul>
        {% endactiveurl %}
    '''

    context = {'request': requests.get('/')}
    html = render(template, context)

    tree = fragment_fromstring(html)
    li_elements = tree.xpath('//li')

    active_li = li_elements[0]

    assert active_li.attrib.get('class', False)
    assert 'active' == active_li.attrib['class']

    inactive_li = li_elements[1]

    assert not inactive_li.attrib.get('class', False)


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

    assert not inactive_li.attrib.get('class', False)


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

    assert active_li.attrib.get('class', False)
    assert 'active' == active_li.attrib['class']

    inactive_li = li_elements[1]

    assert not inactive_li.attrib.get('class', False)


def test_non_ascii_reverse():
    template = '''
        {% activeurl %}
            <ul>
                <li>
                    <a href="/страница/">страница</a>
                </li>
                <li>
                    <a href="{% url 'non-ascii-reverse' %}">другая_страница</a>
                </li>
            </ul>
        {% endactiveurl %}
    '''

    context = {'request': requests.get('/другая_страница/')}
    html = render(template, context)

    tree = fragment_fromstring(html)
    li_elements = tree.xpath('//li')

    active_li = li_elements[1]

    assert active_li.attrib.get('class', False)
    assert 'active' == active_li.attrib['class']

    inactive_li = li_elements[0]

    assert not inactive_li.attrib.get('class', False)


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

    assert active_li.attrib.get('class', False)
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

    assert active_li.attrib.get('class', False)
    assert 'link active' == active_li.attrib['class']


def test_empty_href():
    template = '''
        {% activeurl %}
            <ul>
                <li class="">
                    <a href="">root</a>
                </li>
                <li>
                    <a>root</a>
                </li>
            </ul>
        {% endactiveurl %}
    '''

    context = {'request': requests.get('/')}
    html = render(template, context)

    tree = fragment_fromstring(html)
    li_elements = tree.xpath('//li')

    active_li = li_elements[0]

    assert active_li.attrib.get('class', False)
    assert 'active' == active_li.attrib['class']

    inactive_li = li_elements[1]

    assert not inactive_li.attrib.get('class', False)


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

    assert active_li.attrib.get('class', False)
    assert 'active' == active_li.attrib['class']


def test_cache():
    html = '<ul><li><a href="/page/">page</a></li></ul>'
    template = '{% activeurl %}' + html + '{% endactiveurl %}'

    context = {'request': requests.get('/page/')}
    set_cache = render(template, context)

    cache_key = html + get_cache_params('/page/')
    cache_key = cache_key.encode()
    cache_key = md5(cache_key).hexdigest()

    cache_key = '%s.%s.%s.%s' % (
        settings.ACTIVE_URL_CACHE_PREFIX,
        __version__,
        get_language(),
        cache_key,
    )

    from_cache = cache.get(cache_key)

    assert from_cache

    get_cache = render(template, context)

    assert from_cache == set_cache == get_cache


def test_active_root():
    template = '''
        {% activeurl %}
            <ul>
                <li>
                    <a href="/">root</a>
                </li>
                <li>
                    <a href="/page/">page</a>
                </li>
            </ul>
        {% endactiveurl %}
    '''

    context = {'request': requests.get('/')}
    html = render(template, context)

    tree = fragment_fromstring(html)
    li_elements = tree.xpath('//li')

    active_li = li_elements[0]

    assert 'active' == active_li.attrib['class']

    inactive_li = li_elements[1]

    assert not inactive_li.attrib.get('class', False)


def test_submenu_configuration():
    template = '''
        {% activeurl menu='false' %}
            <ul>
                <li>
                    <a href="/menu/">menu</a>
                </li>
            </ul>
        {% endactiveurl %}

        {% activeurl menu=False %}
            <ul>
                <li>
                    <a href="/menu/">menu</a>
                </li>
            </ul>
        {% endactiveurl %}
        {% activeurl menu=None %}
            <ul>
                <li>
                    <a href="/menu/">menu</a>
                </li>
            </ul>
        {% endactiveurl %}
        {% activeurl menu=True %}
            <ul>
                <li>
                    <a href="/menu/">menu</a>
                </li>
            </ul>
        {% endactiveurl %}
    '''

    context = {'request': requests.get('/menu/submenu/')}
    html = render(template, context)

    tree = fromstring(html)
    li_elements = tree.xpath('//li')

    for inctive_li in li_elements[:-1]:
        assert not inctive_li.attrib.get('class', False)

    active_li = li_elements[-1]

    assert 'active' == active_li.attrib['class']


def test_non_active_root():
    template = '''
        {% activeurl %}
            <ul>
                <li>
                    <a href="/">root</a>
                </li>
                <li>
                    <a href="/page/">page</a>
                </li>
            </ul>
        {% endactiveurl %}
    '''

    context = {'request': requests.get('/page/')}
    html = render(template, context)

    tree = fragment_fromstring(html)
    li_elements = tree.xpath('//li')

    inactive_li = li_elements[0]

    assert not inactive_li.attrib.get('class', False)

    active_li = li_elements[1]

    assert 'active' == active_li.attrib['class']


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

    assert active_menu.attrib.get('class', False)
    assert 'active' == active_menu.attrib['class']

    active_submenu = li_elements[1]

    assert active_submenu.attrib.get('class', False)
    assert 'active' == active_submenu.attrib['class']

    inactive_submenu = li_elements[2]

    assert not inactive_submenu.attrib.get('class', False)


def test_submenu_top_level():
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

    context = {'request': requests.get('/menu/')}
    html = render(template, context)

    tree = fragment_fromstring(html)
    li_elements = tree.xpath('//li')

    active_menu = li_elements[0]

    assert active_menu.attrib.get('class', False)
    assert 'active' == active_menu.attrib['class']

    for inactive_submenu in li_elements[1:]:
        assert not inactive_submenu.attrib.get('class', False)


def test_nested_submenu():
    template = '''
        {% activeurl parent_tag="div" %}
            <div>
                <div>
                    <a href="/menu/">menu</a>
                    <div>
                        <a href="/menu/submenu/">submenu</a>
                    </div>
                    <div>
                        <a href="/menu/other_submenu/">other_submenu</a>
                    </div>
                </div>
            </div>
        {% endactiveurl %}
    '''

    context = {'request': requests.get('/menu/submenu/')}
    html = render(template, context)

    tree = fragment_fromstring(html)
    div_elements = tree.xpath('//div')

    active_menu = div_elements[1]

    assert active_menu.attrib.get('class', False)
    assert 'active' == active_menu.attrib['class']

    active_submenu = div_elements[2]

    assert active_submenu.attrib.get('class', False)
    assert 'active' == active_submenu.attrib['class']

    inactive_submenu = div_elements[3]

    assert not inactive_submenu.attrib.get('class', False)

    inactive_root = div_elements[0]

    assert not inactive_root.attrib.get('class', False)


def test_submenu_no_menu():
    template = '''
        {% activeurl menu='no' %}
            <ul>
                <li>
                    <a href="/menu/submenu/">submenu</a>
                </li>
                <li>
                    <a href="/menu/other_submenu/">other_submenu</a>
                </li>
                <li>
                    <a href="/menu/">menu</a>
                </li>
            </ul>
        {% endactiveurl %}
    '''

    context = {'request': requests.get('/menu/submenu/')}
    html = render(template, context)

    tree = fragment_fromstring(html)
    li_elements = tree.xpath('//li')

    active_menu = li_elements[0]

    assert active_menu.attrib.get('class', False)
    assert 'active' == active_menu.attrib['class']

    for inactive_submenu in li_elements[1:]:
        assert not inactive_submenu.attrib.get('class', False)


def test_malformed_menu():
    template = '''
        {% activeurl menu='hz' %}
            <ul>
                <li>
                    <a href="/menu/">menu</a>
                </li>
                <li>
                    <a href="/menu/submenu/">submenu</a>
                </li>
            </ul>
        {% endactiveurl %}
    '''

    context = {'request': requests.get('/menu/')}
    try:
        render(template, context)
        assert False
    except ImproperlyConfigured:
        pass


def test_no_parent():
    template = '''
        {% activeurl parent_tag=None %}
            <div>
                <a href="/page/">page</a>
            </div>
        {% endactiveurl %}
        {% activeurl parent_tag=False %}
            <div>
                <a href="/page/">page</a>
            </div>
        {% endactiveurl %}
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

    for active_a in a_elements[:-1]:
        assert active_a.attrib.get('class', False)
        assert 'active' == active_a.attrib['class']

    inactive_a = a_elements[-1]

    assert not inactive_a.attrib.get('class', False)


def test_malformed_parent_tag():
    template = '''
        {% activeurl parent_tag=True %}
            <div>
                <a href="/page/">page</a>
            </div>
        {% endactiveurl %}
    '''
    context = {'request': requests.get('/page/')}

    try:
        render(template, context)
        assert False
    except ImproperlyConfigured:
        pass


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

    assert active_menu.attrib.get('class', False)
    assert 'active' == active_menu.attrib['class']

    active_submenu = a_elements[1]

    assert active_submenu.attrib.get('class', False)
    assert 'active' == active_submenu.attrib['class']

    inactive_submenu = a_elements[2]

    assert not inactive_submenu.attrib.get('class', False)


def test_no_parent_cache():
    html = '<div><a href="/page/">page</a></div>'
    template = '{% activeurl parent_tag="self" %}' + html \
        + '{% endactiveurl %}'

    context = {'request': requests.get('/page/')}
    set_cache = render(template, context)

    cache_key = html + get_cache_params('/page/', parent_tag='self')
    cache_key = cache_key.encode()
    cache_key = md5(cache_key).hexdigest()

    cache_key = '%s.%s.%s.%s' % (
        settings.ACTIVE_URL_CACHE_PREFIX,
        __version__,
        get_language(),
        cache_key,
    )

    from_cache = cache.get(cache_key)

    assert from_cache

    from_cache = from_cache

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

    assert active_div.attrib.get('class', False)
    assert 'current' == active_div.attrib['class']

    for inactive_div in div_elements[:-1]:
        assert not inactive_div.attrib.get('class', False)


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

    assert active_p.attrib.get('class', False)
    assert 'highlight' == active_p.attrib['class']

    inactive_p = p_elements[0]

    assert not inactive_p.attrib.get('class', False)


def test_kwargs_multiple_urls_nested_tags():
    template = '''
        {% activeurl parent_tag='tr' css_class='active_row' %}
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

    assert active_tr.attrib.get('class', False)
    assert 'active_row' == active_tr.attrib['class']

    inactive_tr = tr_elements[1]

    assert not inactive_tr.attrib.get('class', False)


def test_basic_again_test_default_settings():
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

    assert active_li.attrib.get('class', False)
    assert 'active' == active_li.attrib['class']

    inactive_li = li_elements[1]

    assert not inactive_li.attrib.get('class', False)


def test_dajngo_template():
    response = client.get('/template/django/')

    html = response.content

    tree = fragment_fromstring(html)
    li_elements = tree.xpath('//li')

    active_li = li_elements[0]

    assert active_li.attrib.get('class', False)
    assert 'active' == active_li.attrib['class']

    inactive_li = li_elements[1]

    assert not inactive_li.attrib.get('class', False)


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


try:
    from jinja2 import Environment, DictLoader

    from django_activeurl.ext.django_jinja import ActiveUrl

    test_basic_jinja = '''
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

    test_no_parent_jinja = '''
        {% activeurl parent_tag=None %}
            <div>
                <a href="/page/">page</a>
            </div>
        {% endactiveurl %}
        {% activeurl parent_tag=False %}
            <div>
                <a href="/page/">page</a>
            </div>
        {% endactiveurl %}
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

    test_kwargs_jinja = '''
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

    test_coma_jinja = '''
        {% activeurl parent_tag='div', css_class='current', %}
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

    env = Environment(
        loader=DictLoader({
            'test_basic_jinja': test_basic_jinja,
            'test_no_parent_jinja': test_no_parent_jinja,
            'test_kwargs_jinja': test_kwargs_jinja,
            'test_coma_jinja': test_coma_jinja,
        }),
        extensions=[ActiveUrl],
    )

    def test_basic_jinja_django():
        template = env.get_template('test_basic_jinja')

        context = {'request': requests.get('/page/')}
        html = template.render(context)

        tree = fragment_fromstring(html)
        li_elements = tree.xpath('//li')

        active_li = li_elements[0]

        assert active_li.attrib.get('class', False)
        assert 'active' == active_li.attrib['class']

        inactive_li = li_elements[1]

        assert not inactive_li.attrib.get('class', False)

    def test_no_parent_jinja_django():
        template = env.get_template('test_no_parent_jinja')

        context = {'request': requests.get('/page/')}
        html = template.render(context)

        tree = fromstring(html)
        a_elements = tree.xpath('//a')

        for active_a in a_elements[:-1]:
            assert active_a.attrib.get('class', False)
            assert 'active' == active_a.attrib['class']

        inactive_a = a_elements[-1]

        assert not inactive_a.attrib.get('class', False)

    def test_kwargs_jinja_django():
        template = env.get_template('test_kwargs_jinja')

        context = {'request': requests.get('/page/')}
        html = template.render(context)

        tree = fragment_fromstring(html)
        div_elements = tree.xpath('//div')

        active_div = div_elements[-1]

        assert active_div.attrib.get('class', False)
        assert 'current' == active_div.attrib['class']

        for inactive_div in div_elements[:-1]:
            assert not inactive_div.attrib.get('class', False)

    def test_coma_jinja_django():
        template = env.get_template('test_coma_jinja')

        context = {'request': requests.get('/page/')}
        html = template.render(context)

        tree = fragment_fromstring(html)
        div_elements = tree.xpath('//div')

        active_div = div_elements[-1]

        assert active_div.attrib.get('class', False)
        assert 'current' == active_div.attrib['class']

        for inactive_div in div_elements[:-1]:
            assert not inactive_div.attrib.get('class', False)

    def test_native_jinja():
        response = client.get('/template/jinja/')

        html = response.content

        tree = fragment_fromstring(html)
        li_elements = tree.xpath('//li')

        active_li = li_elements[1]

        assert active_li.attrib.get('class', False)
        assert 'active' == active_li.attrib['class']

        inactive_li = li_elements[0]

        assert not inactive_li.attrib.get('class', False)


except ImportError:
    # no jinja installed
    pass
