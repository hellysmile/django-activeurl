'''jinja utils'''


# jinja global function
def options(request, **kwargs):
    '''add full_path to kwargs dict'''
    kwargs['full_path'] = request.get_full_path()
    return kwargs
