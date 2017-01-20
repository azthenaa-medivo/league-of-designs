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
    config_collection = database.config

    # Per realm
    CONF_MAX_BATCH = 50
    realms = ['na', 'euw', 'pbe']

    conf = None
    has_work_flag = False
    rioters = set([])
    bulk = None

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
        realm_posts = self.conf.get(realm, [])
        for d in reversed(data):
            if d.get('comment') is None:
                post_id = d['discussion']['id']
            else:
                post_id = d['comment']['discussion']['id'] + ',' + d['comment']['id']
            if post_id not in realm_posts:
                d['post_id'] = post_id
                d['region'] = realm
                # Update conf
                self.has_work_flag = True
                self.bulk.insert(d)
                realm_posts.append(post_id)
                # Find the Rioter
                if 'comment' in d:
                    rioter = d['comment']['user']['name']
                else:
                    rioter = d['discussion']['user']['name']
                print("Adding rioter : " + rioter + " from realm " + realm + ", post : " + post_id)
                self.rioters.add(rioter)
        if len(realm_posts) > self.CONF_MAX_BATCH:
            # Now we remove the last n elements from the bottom of the array (they're sorted by date descending).
            realm_posts = realm_posts[len(realm_posts) - self.CONF_MAX_BATCH:]
        self.conf[realm] = realm_posts

    def get_red_posts_and_store(self, realms=None, parameters=None, mega_bulk=False):
        """Retrieves the latest Red Posts and puts them into the database."""
        if realms is None:
            realms = self.realms
        count = {realm: 0 for realm in realms}
        self.init_red_import()
        for realm in realms:
            data = self.get_red_posts(realm, parameters=parameters).json()
            count[realm] = len(data)
            self.store_red_posts(data, realm, mega_bulk=False)
        self.save_conf()
        return count

    def init_red_import(self):
        self.bulk = self.red_posts_collection.initialize_ordered_bulk_op()
        # Check config 'last_batch' and include those that miss.
        if self.conf is None:
            self.conf = self.config_collection.find_one({'name': 'last_batch'})
            if self.conf is None:
                self.conf = {'name': 'last_batch', 'post_ids': [], 'rioters': self.rioters}
                for realm in self.realms:
                    self.conf[realm] = []

    def save_conf(self):
        # Assemble all realms
        all_posts = []
        for p in [self.conf[realm] for realm in self.realms]:
            all_posts.extend(p)
        self.conf['post_ids'] = list(all_posts)
        self.conf['has_work'] = self.has_work_flag
        self.conf['rioters'] = list(self.rioters)
        self.config_collection.update_one({'name': 'last_batch'}, {'$set': self.conf}, upsert=True)
        try:
            return self.bulk.execute()
        except InvalidOperation:
            print('Nothing to insert !')
            return 0

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
