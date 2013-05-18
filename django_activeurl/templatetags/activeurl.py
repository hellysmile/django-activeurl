'''activeurl django template library with django-classy-tags'''
from hashlib import md5
from django import template
from django.core.cache import cache
from classytags.core import Tag, Options
from classytags.arguments import MultiKeywordArgument
from django_activeurl import settings
from django_activeurl.utils import check_html


register = template.Library()


class ActiveUrl(Tag):
    '''activeurl django template tag with django-classy-tags'''

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

        # accept from template parent_tag values such as False, None, ''
        if not parent_tag:
            parent_tag = 'self'

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
            data = '%s%s%s%s' % (content, css_class, parent_tag, full_path)
            data = data.encode('utf-8', 'ignore')

            cache_key = '%s%s' % (
                settings.CACHE_ACTIVE_URL_PREFIX,
                md5(data).hexdigest()
            )

            from_cache = cache.get(cache_key)

            if from_cache:
                return from_cache

        # render html with activeurl logic
        content = check_html(content, full_path, css_class, parent_tag)

        # write rendered html to cache, if caching is enabled
        if settings.CACHE_ACTIVE_URL:
            cache.set(cache_key, content, settings.CACHE_ACTIVE_URL_TIMEOUT)

        return content

# register new template tag
register.tag(ActiveUrl)
