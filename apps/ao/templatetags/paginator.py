#  Based on: http://www.djangosnippets.org/snippets/73/
#
#  Modified by Sean Reifschneider to be smarter about surrounding page
#  link context.  For usage documentation see:
#
#     http://www.tummy.com/Community/Articles/django-pagination/

from django import template
import re

register = template.Library()

@register.inclusion_tag('paginator.html', takes_context=True)
def paginator(context, adjacent_pages=2, maxchars=9999):
    """
    To be used in conjunction with the object_list generic view.

    Adds pagination context variables for use in displaying first, adjacent and
    last page links in addition to those created by the object_list generic
    view.

    Includes some pretty site specific stuff now. -tom
    """
    request_adjacent_pages = adjacent_pages
    for close_thresshold in [3,2]:
      for adjacent_pages in range(request_adjacent_pages, 0, -1):
          startPage = max(context['page'] - adjacent_pages, 1)
          if startPage <= 3: startPage = 1
          endPage = context['page'] + adjacent_pages + 1
          if endPage >= context['pages'] - 1: endPage = context['pages'] + 1
          page_numbers = [n for n in range(startPage, endPage) \
                  if n > 0 and n <= context['pages']]
          page_obj = context['page_obj']
          paginator = context['paginator']
          show_first = 1 not in page_numbers
          show_last = context['pages'] not in page_numbers

          # figure out how many characters

          ELISPSES_LENGTH = 2

          charcount = 0
          if show_first:
              # assume 3 dots plus 2 spaces
              charcount += 3 + ELISPSES_LENGTH
          if show_last:
              # assume 3 dots plus 2 spaces
              charcount += 2 + ELISPSES_LENGTH  + len(str(context["pages"]))
          for p in page_numbers:
              # digits plus a space
              charcount += len(str(p)) + 1
          if charcount < maxchars:
              break
    return {
        'request': context["request"],
        'page_obj': page_obj,
        'paginator': paginator,
        'hits': context['hits'],
        'results_per_page': context['results_per_page'],
        'page': context['page'],
        'pages': context['pages'],
        'page_numbers': page_numbers,
        'next': context['next'],
        'previous': context['previous'],
        'has_next': context['has_next'],
        'has_previous': context['has_previous'],
        'show_first': show_first,
        'show_last': show_last
    }


@register.tag
def pagelink(parser, token):
    try:
        tagname,pagenum = token.split_contents()
    except:
        raise template.TemplateSyntaxError('%s tag requires 1 arguments' % token.split_contents()[0])
    return PageLinkNode(pagenum)

class PageLinkNode(template.Node):
    def __init__(self, pagenum):
        self.pagenum = template.Variable(pagenum)

    def render(self, context):
        page = self.pagenum.resolve(context)
        path = context["request"].path.split("/")[:-1]
        if re.match("^\d+$",path[-1]):
            path = path[:-1]
        url = "/".join(path + [str(page)]) + "/"
        if context["request"].META["QUERY_STRING"]:
            url += "?" + context["request"].META["QUERY_STRING"]
        return url
