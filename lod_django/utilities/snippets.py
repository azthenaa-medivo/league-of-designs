import datetime
from bson import ObjectId
from json import JSONEncoder
from django.shortcuts import render_to_response
from django.template import RequestContext
from app_database.postimport import postimport as pi
from .templatetags.markdown_extension import QuoteExtension
from markdown import markdown

def render_to(template):
    """
    Decorator for Django views that sends returned dict to render_to_response function
    with given template and RequestContext as context instance.

    If view doesn't return dict then decorator simply returns output.
    Additionally view can return two-tuple, which must contain dict as first
    element and string with template name as second. This string will
    override template name, given as parameter

    Parameters:

     - template: template name to use
    """
    def renderer(func):
        def wrapper(request, *args, **kw):
            output = func(request, *args, **kw)
            if isinstance(output, (list, tuple)):
                return render_to_response(output[1], output[0], RequestContext(request))
            elif isinstance(output, dict):
                return render_to_response(template, output, RequestContext(request))
            return output
        return wrapper
    return renderer

def postimport(script):
    """
    Decorator for the Consumer that executes :arg:script after the function.

    Parameters:

     - script: Mongo Javascript file to execute.
    """
    def execute_script(func):
        def wrapper(request, *args, **kw):
            res = func(request, *args, **kw)
            pi(script)
            return res
        return wrapper
    return execute_script

class JSONObjectIdEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return o.isoformat()
        return JSONEncoder.default(self, o)

def to_markdown(string):
    if string is None:
        return markdown("**Click on the thread link to view this post !**")
    else:
        return markdown(string, extensions=[QuoteExtension()])
