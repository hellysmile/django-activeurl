'''template engine independent utils'''
from lxml.html import fragment_fromstring, fragments_fromstring, tostring
from lxml.etree import ParserError


def check_active(url, el, full_path, css_class, parent_tag):
    '''check url "active" status, apply css_class to html element'''
    # check non empty href parameter
    if url.attrib.get('href'):
        # skip "root" url
        if url.attrib['href'] != '/':
            # compare href parameter with full path
            if full_path.startswith(url.attrib['href']):
                # check parent tag has "class" attribute or it is empty
                if el.attrib.get('class'):
                    # prevent multiple "class" adding
                    if not css_class in el.attrib['class']:
                        # append "active" class
                        el.attrib['class'] += ' ' + css_class
                else:
                    # create or set "class" attribute
                    el.attrib['class'] = css_class
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
        urls = tree.xpath('//a')
        # check "active" status for all urls
        for url in urls:
            if check_active(url, url, full_path, css_class, parent_tag):
                processed = True
    # otherwise css_class must be applied to parent_tag
    else:
        # xpath query to get all parents tags
        els = tree.xpath('//%s' % parent_tag)
        # check all html elements for "active" <a>
        for el in els:
            # xpath query to get all <a> inside current tag
            urls = el.xpath('.//a')
            # check "active" status for all urls
            for url in urls:
                if check_active(url, el, full_path, css_class, parent_tag):
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
        # build html elements tree from html fragment
        tree = fragment_fromstring(content)
        # check html fragment for "active" urls
        check_content = check_fragment(
            tree, full_path, css_class, parent_tag
        )
        if not check_content is False:
            content = check_content
    # not valid html root tag
    except ParserError:
        tree = fragments_fromstring(content)
        # python 3 lxml fix for empty byte strings
        tree = [el for el in tree if not isinstance(el, str)]
        rebuild_content = ''
        processed = False
        # check all multiple tags
        for el in tree:
            check_content = check_fragment(
                el, full_path, css_class, parent_tag
            )
            if not check_content is False:
                rebuild_content = '%s%s' % (
                    rebuild_content,
                    check_content
                )
                processed = True
            else:
                rebuild_content = '%s%s' % (
                    rebuild_content,
                    tostring(el)
                )
        if processed:
            content = rebuild_content
    return content
