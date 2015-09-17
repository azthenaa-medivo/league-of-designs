__author__ = 'artemys'

import re
import datetime
from pymongo import MongoClient, DESCENDING, ASCENDING
from bson.objectid import ObjectId
from utilities.snippets import postimport

class Consumer:
    """We'll get everything using Python EVE later. I've got only
    one server, y'know."""

    def __init__(self, address="127.0.0.1", port=27017):
        self.client = MongoClient(address, port)
        self.champions_collection = self.client.lod.mr_champions
        self.red_posts_collection = self.client.lod.mr_reds
        self.articles_collection = self.client.lod.articles
        self.rioters_collection = self.client.lod.mr_rioters

    def get_champions(self, query={}, projection=None, sort_field='name', sort_order=ASCENDING):
        """Return a simple list of all Champions."""
        return self.champions_collection.find(query, projection).sort(sort_field, sort_order)

    def get_champion(self, query, projection=None):
        """Returns a single champion. If none is found, returns a random champion. (maybe)"""
        # TODO : RANDOM CHAMPION GENERATOR
        return self.champions_collection.find_one(query, projection)

    def get_red_posts(self, query={}, projection=None, limit=10, sort_field='date', sort_order=DESCENDING):
        """Returns the qty last Red Posts."""
        return self.red_posts_collection.find(query, projection).limit(limit).sort(sort_field, sort_order)

    def get_articles(self, query={}, limit=10, projection=None, sort_field='date_created', sort_order=DESCENDING):
        """What could this method do ?"""
        return self.articles_collection.find(query, projection).limit(limit).sort(sort_field, sort_order)

    def get_article(self, query, projection=None):
        """Return A Single Article."""
        return self.articles_collection.find_one(query, projection)

    def update_champion(self, data):
        """Update champion with Mongo id with $set: dict."""
        c_id = data.pop('_id', None)
        return self.champions_collection.update_one({'_id': ObjectId(c_id)}, {'$set': data})

    @postimport('articles_postimport.js')
    def update_article(self, data, auto_pi=True):
        """Update article with Mongo id with $set: data and map it to its related champion if specified.
        Also generates a proper url_id if needed. If auto_pi is True, we will also execute the map/reduce
        operations."""
        article_id = data.pop('_id', None)
        res = {}
        if data['url_id'] in [None, '']:
            data['url_id'] = re.sub(' +', '-', re.sub(r'\W+-', '', data['title']))
        res['url_id'] = data['url_id']
        data['date_modified'] = datetime.datetime.utcnow()
        if article_id == "new":
            data['date_created'] = datetime.datetime.utcnow()
            res['op'] = 'i'
            res['db'] = self.articles_collection.insert(data)
        else:
            res['op'] = 'u'
            res['db'] = self.articles_collection.update({'_id': ObjectId(article_id)}, {'$set': data}, upsert=True)
        return res

    @postimport('articles_postimport.js')
    def remove_article(self, query):
        """Remove whatever article is found by the Query. TO THE DEPTHS."""
        res = self.articles_collection.remove(query)
        return res

    def get_rioters(self, query={}, projection=None, sort_field='name', sort_order=ASCENDING):
        return self.rioters_collection.find(query, projection).sort(sort_field, sort_order)

if __name__ == '__main__':
    c = Consumer()
    # t = [[c['_id'], c['name']] for c in list(c.get_champions(projection={'_id':1, 'name':1}))]
    print(list(c.get_rioters()))