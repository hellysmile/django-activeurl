'''jinja utils'''


# jinja global function
def options(request, **kwargs):
    '''add full_path to kwargs dict'''

    # TODO: flask port
    # try:  # django
    #     kwargs['full_path'] = request.get_full_path()
    # except AttributeError:  # flask
    #     kwargs['full_path'] = request.path

    kwargs['full_path'] = request.get_full_path()
    return kwargs
