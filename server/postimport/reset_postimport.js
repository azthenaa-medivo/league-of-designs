/*
 *  Undo lod_postimport by replacing the added data by empty values.
 *  Executing lod_postimport > reset_postimport has no effect.
 *  Use this script to refresh the database without killing your mr_reds collection.
 */

print('reset:mr_reds[done,champions,champions_data]');

db.mr_reds.update({},
                    {'$set': {
                                'done': 0,
                                'champions': [],
                                'champions_data': [],
                    }},
                    {'multi': 1});

print('reset:mr_champions[red_posts,rioter_counter,glorious_posts,total_posts,]');

db.mr_champions.update({},
                        {'$set': {
                                    'rioter_counter': [],
                                    'glorious_posts': 0,
                                    'total_posts': 0,
                        }},
                        {'multi':1});

print('reset:mr_rioters[posts,last_post,champions_occurrences,]');

db.mr_rioters.update({},
                        {'$set': {
                                    'posts': [],
                                    'last_post': null,
                                    'champions_occurrences': [],
                        }},
                        {'multi':1});