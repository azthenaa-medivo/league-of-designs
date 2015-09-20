__author__ = 'artemys'

import json
from utilities.snippets import render_to, JSONObjectIdEncoder, to_markdown
from app_database.consumer import Consumer
from .models import ARTICLE_TYPE, ROLES, REGIONS, GLORIOUS_SECTIONS
from .forms import ChampionForm, ArticleForm, NewArticleForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required

consumer = Consumer()

@render_to('home.html')
def view_home(request):
    reds = consumer.get_red_posts(limit=5, query={'champions': {'$exists': True, '$ne': []},
                                                  'region': 'NA',
                                                  'section' : {'$in': GLORIOUS_SECTIONS}})
    articles = consumer.get_articles(limit=5, query={'type': 'News'})
    return {'reds': reds, 'articles': articles}

@render_to('red_posts_main.html')
def view_red_posts(request):
    boards_sections = request.GET.get('all')
    if request.is_ajax():
        the_query = {}
        q = request.GET.get('search')
        if q and q != '':
            the_query['$text'] = {'$search': q}
        if not boards_sections:
            the_query['section'] = {'$in': GLORIOUS_SECTIONS}
        else:
            the_query['$or'] = [{'champions': {'$exists': 1}},
                                {'section': {'$in': GLORIOUS_SECTIONS}}]
        reds = consumer.get_red_posts(query=the_query, limit=0)
        data = list(reds)
        for d in data:
            d['contents'] = to_markdown(d['contents'])
        return HttpResponse(JSONObjectIdEncoder().encode({'data': data}), content_type='application/json')
    rioters = consumer.get_rioters()
    return {'rioters': rioters, 'all': not not boards_sections, 'regions': zip(REGIONS, REGIONS)} # TRICK SHOT

@render_to('about.html')
def view_about(request):
    return {}

@render_to('champion.html')
def view_champion(request, url_id):
    champion = consumer.get_champion({'url_id':url_id})
    if champion is None:
        return HttpResponseRedirect('/')
    return {'champion': champion, 'regions': zip(REGIONS, REGIONS)}

@render_to('champions_grid.html')
def view_champions_grid(request):
    return {'roles': zip(ROLES, ROLES)}

@login_required
@render_to('champion_edit.html')
def edit_champion(request, url_id):
    champion = consumer.get_champion({'url_id':url_id})
    if champion is None:
        return {'champion': {'name':'Kappa'}}
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
def view_rioters(request):
    rioters = consumer.get_rioters()
    return {'rioters': rioters}

@render_to('article.html')
def view_article(request, article_id):
    article = consumer.get_article({'url_id': article_id})
    return {'article': article}

@render_to('articles_main.html')
def view_articles_list(request):
    articles = consumer.get_articles()
    return {'articles': articles, 'types': ARTICLE_TYPE}

@login_required
@render_to('article_edit.html')
def edit_article(request, article_id):
    # Okay *maybe* a bit of cleanup would be <good>... <GOOD VERY GOOD ONE MORE!!!!>
    champion = None
    context = {}
    # If we're saving an article
    if request.method == 'POST':
        if request.POST.get('champion') is not None:
            champion = consumer.get_champion({'url_id': request.GET.get('champion')})
        form = ArticleForm(request.POST)
        if form.is_valid():
            o = form.save()
            # Check if we updated or inserted
            if o['op'] == 'i':
                r_url = reverse('article-edit', kwargs={'article_id': o['url_id']})
                return HttpResponseRedirect(r_url + '?success=1')
            else:
                form = ArticleForm(request.POST)
                messages.add_message(request, messages.SUCCESS, 'Article was correctly updated !', extra_tags='text-success')
        else:
            messages.add_message(request, messages.ERROR, 'There was an issue with this article !', extra_tags='text-danger')
    else:
        if request.GET.get('champion') is not None:
            # Article about a champion
            champion = consumer.get_champion({'url_id': request.GET.get('champion')})
        if request.GET.get('success') is not None:
            messages.add_message(request, messages.SUCCESS, 'Article was successfully created !', extra_tags='text-success')
        article = consumer.get_article({'url_id': article_id})
        if article is None:
            form = NewArticleForm({'champion': champion['_id'] if champion is not None else None, 'url_id': article_id,
                                   '_id': "new"})
        else:
            form = ArticleForm(article)
    return {'champion': champion, 'form': form, 'article_id': article_id}

@login_required
@render_to('article_kill.html')
def kill_article(request, article_id):
    article = consumer.get_article(query={'url_id': article_id})
    if article is not None:
        if request.method == 'GET':
            return {'next': request.GET.get('next'), 'article': article}
        if request.method == 'POST':
            consumer.remove_article(query={'url_id': article_id})
            messages.add_message(request, messages.SUCCESS, "Article " + article['title'] + " was successfully ANNIHILATED. Rejoice !",  extra_tags='text-success')
            return HttpResponseRedirect(request.POST.get('next'))
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
    articles = consumer.get_articles()
    return {'articles': articles}