'''template engine independent utils'''
from lxml.html import fragment_fromstring, tostring
from lxml.etree import ParserError


class ImproperlyConfigured(Exception):
    pass


def check_active(url, element, full_path, css_class):
    '''check url "active" status, apply css_class to html element'''
    # check non empty href parameter
    if url.attrib.get('href'):
        # skip "root" url, otherwise it is will be "active" always
        if url.attrib['href'] != '/':
            # compare href parameter with full path
            if full_path.startswith(url.attrib['href']):
                # check parent tag has "class" attribute or it is empty
                if element.attrib.get('class'):
                    # prevent multiple "class" adding
                    if not css_class in element.attrib['class']:
                        # append "active" class
                        element.attrib['class'] += ' ' + css_class
                else:
                    # create or set "class" attribute
                    element.attrib['class'] = css_class
                return True
    return False


def check_fragment(tree, full_path, css_class, parent_tag):
    '''check html element fragment for "active" urls'''
    # flag for prevent html rebuilding, when no "active" urls found
    processed = False
    # if parent_tag is False\None\empty\a\self
    # "active" status will be applied directly to <a>
    if not parent_tag or parent_tag in ('a', 'self'):
        # xpath query to get all <a>
        urls = tree.xpath('.//a')
        # check "active" status for all urls
        for url in urls:
            if check_active(url, url, full_path, css_class):
                processed = True
    # otherwise css_class must be applied to parent_tag
    else:
        # xpath query to get all parents tags
        elements = tree.xpath('.//%s' % parent_tag)
        # check all html elements for "active" <a>
        for element in elements:
            # xpath query to get all <a> inside current tag
            urls = element.xpath('.//a')
            # check "active" status for all urls
            for url in urls:
                if check_active(url, element, full_path, css_class):
                    # flag for rebuilding html tree
                    processed = True
                    # stop checking other <a> inside current parent_tag
                    break
    # do not rebuild html if no "active" urls inside parent_tag
    if processed:
        # build html from tree
        return tostring(tree)
    # no "active" urls found
    return False


def check_html(content, full_path, css_class, parent_tag):
    '''build html tree from content inside template tag'''
    # valid html root tag
    try:
        # build elements tree from html fragment
        tree = fragment_fromstring(content)
        # check html fragment for "active" urls
        check_content = check_fragment(
            tree, full_path, css_class, parent_tag
        )
        # prevent change content if no "active" urls found
        if not check_content is False:
            content = check_content
    # not valid html root tag
    except ParserError:
        raise ImproperlyConfigured('''
            html inside {% activeurl %} must have valid html root tag
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
            in this case <ul> is valid html root tag
        ''')
    return content
