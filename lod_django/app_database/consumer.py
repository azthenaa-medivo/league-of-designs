__author__ = 'artemys'

import re
import datetime
from pymongo import MongoClient, DESCENDING, ASCENDING
from bson.objectid import ObjectId
from utilities.snippets import postimport

class MongoConsumer:
    """We'll get everything using Python EVE later. I've got only
    one server, y'know."""

    def __init__(self, database, address="127.0.0.1", port=27017):
        """Connect to a Database."""
        self.client = MongoClient(address, port)
        self.database = self.client[database]

    def get_collection(self, collection):
        return self.database[collection]

    def get(self, collection, query={}, projection=None, limit=0, sort_field='_id', sort_order=ASCENDING, *args, **kwargs):
        return self.get_collection(collection).find(query, projection, *args, **kwargs).limit(limit).sort(sort_field, sort_order)

    def get_one(self, collection, query={}, projection=None, *args, **kwargs):
        return self.get_collection(collection).find_one(query, projection, *args, **kwargs)

class LoDConsumer(MongoConsumer):
    def update_champion(self, data):
        """Update champion with Mongo id with $set: dict."""
        c_id = data.pop('_id', None)
        return self.database.mr_champions.update_one({'_id': ObjectId(c_id)}, {'$set': data})

    @postimport('articles_postimport.js')
    def update_article(self, data):
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
            res['db'] = self.database.articles.insert(data)
        else:
            res['op'] = 'u'
            res['db'] = self.database.articles.update({'_id': ObjectId(article_id)}, {'$set': data}, upsert=True)
        return res

    @postimport('articles_postimport.js')
    def remove_article(self, query):
        """Remove whatever article is found by the Query. TO THE DEPTHS."""
        res = self.database.articles.remove(query)
        return res

if __name__ == '__main__':
    c = MongoConsumer('lod')
    print(list(c.get('mr_champions')))