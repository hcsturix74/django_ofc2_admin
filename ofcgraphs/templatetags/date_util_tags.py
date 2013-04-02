from django import template
from django.utils.safestring import mark_safe
import re


register = template.Library()


@register.simple_tag
def format_date_range(from_date, to_date):
    """
    >>> import datetime
    >>> format_date_range(datetime.date(2009,1,15), datetime.date(2009,1,20))
    '15. - 20.01.2009.'
    >>> format_date_range(datetime.date(2009,1,15), datetime.date(2009,2,20))
    '15.01. - 20.02.2009.'
    >>> format_date_range(datetime.date(2009,1,15), datetime.date(2010,2,20))
    '15.01.2009. - 20.02.2010.'
    >>> format_date_range(datetime.date(2009,1,15), datetime.date(2010,1,20))
    '15.01.2009. - 20.01.2010.'

    Use in django templates:
    {% format_date_range exhibition.start_on exhibition.end_on %}
    """
    from_format = to_format = "%Y%m%d"
    return "-".join((from_date.strftime(from_format), to_date.strftime(to_format), ))


class DateRangeNode(template.Node):
    def __init__(self, start_date, end_date, format_string):
        self.start_date = template.Variable(start_date)
        self.end_date = template.Variable(end_date)
        self.format = {}
        if not len(format_string) == 0:
            format_string = format_string.encode('utf-8').strip("\"")
            self.format['day'], self.format['month'], self.format['year'] = format_string.split()
        else:
            self.format['day'], self.format['month'], self.format['year'] = "%d", "%m", "%Y"


def render(self, context):
    try:
        start_date = self.start_date.resolve(context)
        end_date = self.end_date.resolve(context)
    except template.VariableDoesNotExist:
        return ''

    start_format = ""
    end_format = ""
    if start_date.day == end_date.day:
        end_format = self.format['day']
    else:
        start_format = self.format['day']
        end_format = self.format['day']

    if start_date.month == end_date.month:
        end_format += " " + self.format['month']
    else:
        start_format += " " + self.format['month']
        end_format += " " + self.format['month']

    if start_date.year == end_date.year:
        end_format += " " + self.format['year']
    else:
        start_format += " " + self.format['year']
        end_format += " " + self.format['year']
    return start_date.strftime(start_format) + " - " + end_date.strftime(end_format)


def do_date_range(parser, token):
    """ formats two dates as a date range
    eg.
    January 1st 2009 to January 5th 2009
    would result in:
    1 - 5 January 2009

    template usage:

    {% date_range start_date end_date [format string] %}

    """
    chunks = token.split_contents()
    if not len(chunks) >= 3:
        raise template.TemplateSyntaxError, "%r tag requires two or three arguments" % token.contents.split()[0]
    if not len(chunks) <= 4:
        raise template.TemplateSyntaxError, "%r tag requires two or three arguments" % token.contents.split()[0]
    if len(chunks) == 4:
        format = chunks[3]
    else:
        format = ""
    return DateRangeNode(chunks[1], chunks[2], format)

register.tag('date_range', do_date_range)


