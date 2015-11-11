import datetime
import re
from bson import ObjectId
from json import JSONEncoder
from django.core.urlresolvers import reverse
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

def url_idize(str, regex):
    return regex.sub('', str)

def build_red_title(request, consumer):
    """Build at title for the Red Posts page. Just to avoid clogging the view, I'll put the mess here."""
    title = 'The Red Posts'
    n = [k for k, v in request.items() if bool(v) and k != 'is_and']
    if len(n) > 0:
        if 'thread_id' in request and request['thread_id'] != '':
            thread = consumer.get_one('mr_reds', {'thread_id': {'$regex': '^'+request['thread_id']+'$'}},
                                      {'thread': 1, 'url': 1, 'thread_id': 1})
            if thread:
                title = 'Rundown for thread [« %s »](%s)&nbsp;<span class="among-bonus" markdown="1">(ID : %s)</span>'\
                        % (thread['thread'], thread['url'], thread['thread_id'])
        elif 'search' in request and request['search'] != '':
            title = 'Results for search « **%s** » in Red Posts' % request['search']
        elif 'champions' in request and len(request['champions']) > 0:
            r = re.compile('\W')
            title = 'Looking for ' + ', '.join('['+c+']('+reverse('champion', kwargs={'url_id': url_idize(c, r)})+')'
                                               for c in request['champions']) + ' in the Red Posts'
        if len(n) > 1:
            title_title = [k.capitalize() + ' : ' + (str(request[k]) if type(request[k]) in [str, int, bool]
                           else request[k].strftime("%x") if type(request[k]) == datetime.datetime
                           else ', '.join(request[k])) for k in n]
            title += '... <span class="cursorHelp among-bonus" title="'+' / '.join(title_title)+\
                     '" markdown="1">among other things</span>.'
    return to_markdown(title)
