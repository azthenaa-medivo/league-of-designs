from __future__ import unicode_literals
from django import template
from markdown import markdown
from .markdown_extension import QuoteExtension
from app_lod.models import STATUS_MESSAGES
from datetime import datetime

register = template.Library()

@register.filter(name="get")
def get_filter(d, k):
    return d.get(k, None)

@register.filter(name="int")
def integer_filter(i):
    try:
        return int(i)
    except ValueError:
        return i

@register.filter(name="markdown")
def to_markdown(string):
    if string is None:
        return markdown("**LoD has encountered an error processing this post ! Rito pls fix**")
    else:
        return markdown(string, extensions=[QuoteExtension()])

@register.filter(name="status")
def status(string):
    return STATUS_MESSAGES[string]

@register.filter(name="isoformat")
def isoformat(date):
    if type(date) is datetime:
        return date.isoformat()
    else:
        return date

@register.simple_tag
def active_page(request, view_name):
    from django.core.urlresolvers import resolve, Resolver404
    if not request:
        return ""
    try:
        return "active" if resolve(request.path_info).url_name.startswith(view_name) else ""
    except Resolver404:
        return ""

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