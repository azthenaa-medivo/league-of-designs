#!/usr/bin/env python

import copy
import requests
from pymongo import MongoClient
from pymongo.errors import InvalidOperation
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
    red_posts_tmp_collection = database.reds_tmp
    config_collection = database.config

    CONF_MAX_BATCH = 150
    realms = ['na', 'euw', 'pbe']

    def get_champions(self):
        """Fetches the champion pool."""
        url_champions = 'https://global.api.pvp.net/api/lol/static-data/euw/v1.2/champion'
        fields = 'altimages,blurb,image,info,lore,partype,passive,spells,tags'
        return requests.get(url_champions, params={'champData': fields, 'api_key': self.key}).json()['data']

    def get_champions_and_store(self):
        """Collects the champion pool and stores it."""
        champ_data = self.get_champions()
        self.champion_collection.insert_many([d for c, d in champ_data.items()])

    def get_red_posts(self, realm='na', parameters=None):
        """Retrieves the latest Red Posts."""
        return requests.get('http://boards.'+realm+'.leagueoflegends.com/en/redtracker.json', params=parameters)

    def store_red_posts(self, data, realm, mega_bulk=False):
        """Stores Red Posts. Currently broken for main thread contents (waiting for Riot's fix)."""
        if len(data) == 0:
            print('Nothing to insert for realm "%s" !' % realm)
            return 0
        self.red_posts_tmp_collection.remove({})
        bulk = self.red_posts_collection.initialize_ordered_bulk_op()
        # Check config 'last_batch' and include those that miss.
        # For the moment we don't care about posts edits. We will. Worry not.
        conf = self.config_collection.find_one({'name': 'last_batch'})
        rioters = set()
        flag_update_conf = False
        if conf is None:
            conf = {'name': 'last_batch', 'post_ids': []}
        for d in reversed(data):
            if d.get('comment') is None:
                post_id = d['discussion']['id']
            else:
                post_id = d['comment']['discussion']['id'] + ',' + d['comment']['id']
            if post_id not in conf['post_ids']:
                d['post_id'] = post_id
                d['region'] = realm
                bulk.insert(d)
                # Update conf
                flag_update_conf = True
                conf['post_ids'].append(post_id)
                if 'comment' in d:
                    rioters.add(d['comment']['user']['name'])
                else:
                    rioters.add(d['discussion']['user']['name'])
        if len(conf['post_ids']) > self.CONF_MAX_BATCH:
            # Now we remove the last n elements from the bottom of the array (they're sorted by date descending).
            conf['post_ids'] = conf['post_ids'][len(conf['post_ids']) - self.CONF_MAX_BATCH:]
        conf['has_work'] = flag_update_conf
        conf['rioters'] = list(rioters)
        self.config_collection.update_one({'name': 'last_batch'}, {'$set': conf}, upsert=True)
        try:
            return bulk.execute()
        except InvalidOperation:
            print('Nothing to insert for realm "%s" !' % realm)
            return 0

    def get_red_posts_and_store(self, realms=None, parameters=None, mega_bulk=False):
        """Retrieves the latest Red Posts and puts them into the database."""
        if realms is None:
            realms = self.realms
        count = {realm: 0 for realm in realms}
        for realm in realms:
            data = self.get_red_posts(realm, parameters=parameters).json()
            count[realm] = len(data)
            self.store_red_posts(data, realm, mega_bulk=False)
        return count

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
        r.get_champions_and_store()
    if 'r' in args.mode:
        print('get:red-posts')
        r.get_red_posts_and_store()
