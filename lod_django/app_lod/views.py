__author__ = 'artemys'

import ast
import json
from utilities.snippets import render_to, JSONObjectIdEncoder, to_markdown, build_red_title, return_simple_ajax
from app_database.consumer import LoDConsumer
from .lod_ssp import RedPostsSSP, RioterSSP
from .models import ARTICLE_TYPE, ROLES, REGIONS, GLORIOUS_SECTIONS
from .forms import ChampionForm, ArticleForm, NewArticleForm, RedPostDetailedSearchForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template import RequestContext
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from pymongo import DESCENDING

consumer = LoDConsumer('lod')

@render_to('home.html')
def view_home(request):
    home_page = consumer.get_one('config', query={'name': 'home_page'})
    return {'data': home_page}

@render_to('red_posts_main.html')
def view_red_posts(request):
    if request.is_ajax():
        collection = 'mr_reds'
        database = 'lod'
        results = RedPostsSSP(request, database, collection).output_result()
        return HttpResponse(JSONObjectIdEncoder().encode(results), content_type='application/json')
    param_is_and = True
    get_data = {}
    if len(request.GET) != 0:
        param_is_and = False
        form = RedPostDetailedSearchForm(request.GET)
        get_data = form.cleaned_data if form.is_valid() else None
    return {'get_data': get_data, 'param_is_and': param_is_and, 'g_sections': GLORIOUS_SECTIONS,
            'regions': zip(REGIONS, REGIONS), 'red_title': build_red_title(get_data, consumer),
            'filter_rioter_ajax_url': 'rioters', 'filter_rioter_params': '{projection: {name: 1, url_id: 1, total_posts: 1}}'}

@render_to('red_posts_search.html')
def view_red_posts_search(request):
    return {'form': RedPostDetailedSearchForm()}

@render_to('about.html')
def view_about(request):
    return {}

@render_to('champion.html')
def view_champion(request, url_id):
    champion = consumer.get_one('mr_champions', query={'url_id': url_id})
    if champion is None:
        messages.add_message(request, messages.INFO, "Looks like champion %s hasn't been released yet." % url_id)
        return HttpResponseRedirect('/')
    # rioters_for_champ = consumer.get('mr_rioters', query={'champions_occurrences.name': champion['name']})
    return {'champion': champion, 'regions': zip(REGIONS, REGIONS), 'g_sections': GLORIOUS_SECTIONS,
            'filter_champion_page': True}

@render_to('champions_grid.html')
def view_champions_grid(request):
    if request.is_ajax():
        if request.GET.get('args'):
            data = json.loads(request.GET.get('args'))
            champions = list(consumer.get('mr_champions', projection=data['projection']))
            for c in champions:
                c['DT_RowAttr'] = {'data-href': reverse('champion', kwargs={'url_id': c['url_id']})}
            return HttpResponse(JSONObjectIdEncoder().encode({'data': champions}), content_type='application/json')
    # champions = consumer.get('mr_champions', sort_field="name")
    # return {'champions': champions, 'roles': zip(ROLES, ROLES)}
    return {'roles': zip(ROLES, ROLES)}

@login_required
@render_to('champion_edit.html')
def edit_champion(request, url_id):
    champion = consumer.get_one('mr_champions', query={'url_id':url_id})
    if champion is None:
        return {'champion': {'name': 'Kappa'}}
    if request.method == 'POST':
        form = ChampionForm(request.POST)
        if form.is_valid():
            messages.add_message(request, messages.SUCCESS, 'Champion '+champion['name']+' was successfully updated !',
                                 extra_tags='text-success')
            form.save()
        else:
            messages.add_message(request, messages.ERROR, 'There was an error updating the champion. Try again !',
                                extra_tags='text-danger')
    else:
        form = ChampionForm(champion)
    return {'champion': champion, 'form': form}

@render_to('rioters.html')
@return_simple_ajax("mr_rioters", consumer)
def view_rioters(request):
    if request.is_ajax():
        collection = 'mr_rioters'
        database = 'lod'
        rioters = RioterSSP(request, database, collection)
        results = rioters.output_result()
        return HttpResponse(JSONObjectIdEncoder().encode(results), content_type='application/json')
    return {}

@render_to('rioter.html')
def view_rioter(request, rioter_url_id):
    rioter = consumer.get_one('mr_rioters', query={'url_id': rioter_url_id})
    return {'rioter': rioter, 'g_sections': GLORIOUS_SECTIONS, 'simple_rioter': 1, 'filter_rioter_page': True}

@render_to('article.html')
def view_article(request, article_id):
    article = consumer.get_one('articles', query={'url_id': article_id})
    return {'article': article}

@render_to('articles_main.html')
def view_articles_list(request):
    articles = consumer.get('articles')
    return {'articles': articles, 'types': ARTICLE_TYPE}

@login_required
@render_to('article_edit.html')
def edit_article(request, article_id):
    # Okay *maybe* a bit of cleanup would be <good>... <GOOD VERY GOOD ONE MORE!!!!> ahaha.wav
    champion = None
    article = None
    # If we're saving an article
    if request.method == 'POST':
        if request.POST.get('champion') is not None:
            champion = consumer.get_one('mr_champions', query={'url_id': request.GET.get('champion')})
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.setup()
            o = form.save()
            article_id = ''
            # Check if we updated or inserted
            if o.upserted_id is not None:
                # For some reason it's never "upserted" (despite being)... I'll check on this issue later.
                # TODO: See why data is never "upserted" (despite being upserted with ``upsert=True``).
                messages.add_message(request, messages.SUCCESS, 'Article was successfully created !', extra_tags='text-success')
                article_id = reverse('article-edit', kwargs={'article_id': form.cleaned_data['url_id']})
            else:
                article_id = form.cleaned_data['url_id']
                messages.add_message(request, messages.SUCCESS, 'Article was correctly updated !', extra_tags='text-success')
            return HttpResponseRedirect(article_id)
        else:
            messages.add_message(request, messages.ERROR, 'There was an issue with this article !', extra_tags='text-danger')
    else:
        if request.GET.get('champion') is not None:
            # Article about a champion
            champion = consumer.get_one('mr_champions', query={'url_id': request.GET.get('champion')})
        article = consumer.get_one('articles', query={'url_id': article_id})
        if article is None:
            form = NewArticleForm({'champion': champion['name'] if champion is not None else None, 'url_id': article_id,
                                   '_id': "new"})
        else:
            form = ArticleForm(article)
    return {'champion': champion, 'form': form, 'article_id': article_id, 'article': article}

@login_required
@render_to('article_kill.html')
def kill_article(request, article_id):
    article = consumer.get_one('articles', query={'url_id': article_id})
    if article is not None:
        if request.method == 'GET':
            return {'next': request.GET.get('next'), 'article': article}
        if request.method == 'POST':
            consumer.remove_article(query={'url_id': article_id})
            messages.add_message(request, messages.SUCCESS, "Article " + article['title'] + " was successfully ANNIHILATED. Rejoice !",  extra_tags='text-success')
            return HttpResponseRedirect(reverse('articles-list'))
    else:
        return HttpResponseRedirect('/')

def view_logout(request):
    logout(request)
    messages.add_message(request, messages.WARNING, 'See you later !', extra_tags='text-warning')
    return HttpResponseRedirect(request.GET.get('next'))

def view_login(request):
    username = ''
    next = request.GET.get('next', '/')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        next = request.POST.get('next', '/')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.add_message(request, messages.SUCCESS, 'Welcome, ' + username + ' !', extra_tags='text-success')
                return HttpResponseRedirect(next)
            else:
                messages.add_message(request, messages.WARNING, 'User '+username+' has been deactivated.', extra_tags='text-warning')
        else:
            messages.add_message(request, messages.ERROR, 'Something went wrong with the provided credentials.', extra_tags='text-danger')
    return render(request, "login.html", context=RequestContext(request, {'username': username,
                                                                          'next': next}))

@render_to('sitemap.html')
def view_sitemap(request):
    """RENDER ALL THE DATA"""
    articles = consumer.get('articles')
    champions = consumer.get('mr_champions', projection={'name': 1, 'url_id': 1})
    return {'articles': articles, 'champions': champions}
