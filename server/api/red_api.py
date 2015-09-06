#!/usr/bin/env python

import requests
from pymongo import MongoClient
from key import THE_KEY

class RiotAPI:
    """This is the module that retrieves everything !
    While static data is the same for every server (or so we hope),
    Red Posts differ from one region to another - so we have to
    check them thoroughly."""

    key = THE_KEY
    database_server = 'localhost'
    database_port = 27017

    mongo_client = MongoClient(database_server, database_port)
    database = mongo_client.lod
    champion_collection = database.champions
    red_posts_collection = database.reds

    def get_champions(self):
        """Collects the champion pool and stores it."""
        url_champions = 'https://global.api.pvp.net/api/lol/static-data/euw/v1.2/champion'
        fields = 'altimages,blurb,image,info,lore,partype,passive,spells,tags'
        champ_data = requests.get(url_champions, params={'champData': fields, 'api_key': self.key}).json()['data']
        self.champion_collection.insert_many([d for c, d in champ_data.items()])

    def get_redposts(self):
        """Retrieves the latest Red Posts and puts them into the database."""
        bulk = self.red_posts_collection.initialize_ordered_bulk_op()
        region_redposts = ['na', 'euw']
        for region in region_redposts:
            data = requests.get('http://boards.'+region+'.leagueoflegends.com/en/redtracker.json').json()
            for d in data:
                d.update({'region':region})
                post_id = ''
                if d.get('comment') is None:
                    post_id = d['discussion']['id']
                else:
                    post_id = d['comment']['discussion']['id'] + ',' + d['comment']['id']
                d['post_id'] = post_id
                bulk.find({'post_id': post_id}).upsert().update({'$set': d})
        bulk.execute()

    def flush(self):
        self.champion_collection.drop()
        self.red_posts_collection.drop()

    # TODO: Versions of the Champions for the Patch timeline. Currently (9/6/2015) yields a 503.
    #url_versions = 'https://global.api.pvp.net/api/lol/static-data/euw/v1.2/versions'

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', help="c for champions, r for red posts (rc for both)")
    # Mode c imports champion, r red posts.
    args = parser.parse_args()
    if 'c' not in args.mode and 'r' not in args.mode:
        print('Nothing to do here.')
        exit()
    r = RiotAPI()
    if 'c' in args.mode:
        print('get:champions')
        r.get_champions()
    if 'r' in args.mode:
        print('get:red-posts')
        r.get_redposts()