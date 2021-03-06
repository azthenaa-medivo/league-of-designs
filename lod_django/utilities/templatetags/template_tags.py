from __future__ import unicode_literals

import operator
from .markdown_extension import QuoteExtension
from django import template
from markdown import markdown
from app_lod.models import STATUS_MESSAGES
from utilities.snippets import to_markdown
from datetime import datetime

register = template.Library()

@register.filter(name="portrait")
def get_portrait(champ):
    return champ["url_id"] + ".png"

@register.filter(name="get")
def get_filter(d, k):
    return d.get(k, None)

@register.filter(name="plural")
def print_s(l):
    if l > 1:
        return "s"
    else:
        return ""

@register.filter(name="print_js")
def print_rightfully(data):
    if isinstance(data, datetime):
        return '"'+data.strftime("%d/%m/%Y")+'"'
    if isinstance(data, str):
        return '"'+data+'"'
    if isinstance(data, bool):
        return str(data).lower()
    return data

@register.filter(name="int")
def integer_filter(i):
    try:
        return int(i)
    except ValueError:
        return i

@register.filter(name="to_epoch_s")
def to_epoch_s(d):
    if isinstance(d, datetime):
        return int(d.strftime('%s'))*1000

@register.filter(name="markdown")
def to_markdown_wrapper(string):
    return to_markdown(string)

@register.filter(name="status")
def status(string):
    return STATUS_MESSAGES[string]

@register.filter(name="top")
def get_first_n(array, n):
    return array[0:n]

@register.filter(name="favourite_champions")
def favourite(rioter, number=1):
    if 'champions_occurrences' not in rioter:
        return None
    if number == 1:
        if len(rioter['champions_occurrences']) >= 1:
            return sort(rioter['champions_occurrences'], 'count')[-1]
        else:
            return None
    return sort(rioter['champions_occurrences'], 'count')[-number:]

@register.filter(name="join")
def status(a, j):
    return j.join(a) if type(a) == list else a

@register.filter(name="isoformat")
def isoformat(date):
    if type(date) is datetime:
        return date.isoformat()
    else:
        return date

@register.filter(name="sort")
def sort(the_list, key):
    the_list.sort(key=operator.itemgetter(key))
    return the_list

@register.simple_tag
def active_page(request, view_name):
    from django.urls import resolve, Resolver404
    if not request:
        return ""
    try:
        return "active" if resolve(request.path_info).url_name.startswith(view_name) else ""
    except Resolver404:
        return ""

@register.filter(name="last")
def get_last(array):
    array.sort(key=operator.itemgetter('date'))
    return array[-1]

@register.filter(name="wiki_link")
def get_wiki_link(champion):
    link = "http://leagueoflegends.wikia.com/wiki/"+champion['name'].replace(' ', '_')
    return link

@register.filter
def truncatesmart(value, limit=80):
    """
    Truncates a string after a given number of chars keeping whole words.

    Usage:
        {{ string|truncatesmart }}
        {{ string|truncatesmart:50 }}
    """

    try:
        limit = int(limit)
    # invalid literal for int()
    except ValueError:
        # Fail silently.
        return value

    # Make sure it's unicode, PYTHON 3 : YOHO
    # value = value

    # Return the string itself if length is smaller or equal to the limit
    if len(value) <= limit:
        return value

    # Cut the string
    value = value[:limit]

    # Break into words and remove the last
    words = value.split(' ')[:-1]

    # Join the words and return
    return ' '.join(words) + '...'
