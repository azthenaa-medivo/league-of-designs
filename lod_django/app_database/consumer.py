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

    def insert(self, collection, data, *args, **kwargs):
        return self.get_collection(collection).insert(data, *args, **kwargs)

    def update(self, collection, query, data, multi=False, *args, **kwargs):
        """Updates in ``collection`` something that matches ``query`` with ``data``. One."""
        if multi:
            return self.get_collection(collection).update_many(query, data, *args, **kwargs)
        else:
            return self.get_collection(collection).update_one(query, data, *args, **kwargs)

class LoDConsumer(MongoConsumer):
    def update_champion(self, data):
        """Update champion with Mongo id with $set: dict."""
        c_id = data.pop('_id', None)
        return self.database.mr_champions.update_one({'_id': ObjectId(c_id)}, {'$set': data})

    @postimport('articles_postimport.js')
    def update_article(self, query, data, multi=False, *args, **kwargs):
        """Update article, wrapper for the @postimport."""
        return self.update('articles', query, data, multi=multi, upsert=True, *args, **kwargs)

    @postimport('articles_postimport.js')
    def remove_article(self, query):
        """Remove whatever article is found by the Query. TO THE DEPTHS."""
        return self.database.articles.remove(query)

if __name__ == '__main__':
    from random import random
    c = LoDConsumer('test')
    print(c.update_one('test', {'name': 'CRONTABED'}, {'$set': {'kappa': 'PRIDE' + str(int(random()*45))}}))
