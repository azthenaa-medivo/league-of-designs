from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse
from app_database.consumer import Consumer

c = Consumer()

class ChampionSitemap(Sitemap):
    changefreq = "daily"

    def items(self):
        return c.get_champions()

    def location(self, item):
        return reverse('champion', args=[item['url_id']])

class ArticleSitemap(Sitemap):
    changefreq = "daily"

    def items(self):
        return c.get_articles()

    def location(self, item):
        return reverse('article-view', args=[item['url_id']])

class StaticSitemap(Sitemap):
    changefreq = "daily"

    def items(self):
        return ['about', 'red-posts', 'articles-list']

    def location(self, item):
        return reverse(item)