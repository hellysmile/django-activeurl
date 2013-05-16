'''template engine independent utils'''


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
