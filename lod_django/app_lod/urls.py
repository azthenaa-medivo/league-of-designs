"""league_of_designs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    url(r'^$', views.view_home, name="home"),
    url(r'^about$', views.view_about, name="about"),
    url(r'^red-posts$', views.view_red_posts, name="red-posts"),
    url(r'^red-posts/search$', views.view_red_posts_search, name="red-posts-search"),
    url(r'^rioters$', views.view_rioters, name="rioters"),
    url(r'^rioter/(?P<rioter_url_id>[\w]*)$', views.view_rioter, name="rioter"),
    url(r'^champions$', views.view_champions_grid, name="champions-grid"),
    url(r'^champion/(?P<url_id>[\w]*)$', views.view_champion, name="champion"),
    url(r'^champion/(?P<url_id>[\w]+)/edit$', views.edit_champion, name="champion-edit"),
    url(r'^article/edit/(?P<article_id>[\w-]+)$', views.edit_article, name="article-edit"),
    url(r'^article/read/(?P<article_id>[\w-]+)$', views.view_article, name="article-view"),
    url(r'^article/kill/(?P<article_id>[\w-]+)$', views.kill_article, name="article-kill"),
    url(r'^articles$', views.view_articles_list, name="articles-list"),
    url(r'^login$', views.view_login, name="login"),
    url(r'^logout$', views.view_logout, name="logout"),
    url(r'^sitemap$', views.view_sitemap, name="sitemap"),
    url(r'^admin/$', include(admin.site.urls)),
    url(r'.*', RedirectView.as_view(url='/')),
]
