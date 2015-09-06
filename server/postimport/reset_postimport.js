/*
 *  Undo lod_postimport by replacing the added data by empty values.
 *  Executing lod_postimport > reset_postimport has no effect.
 *  Use this script to refresh the database without killing your mr_reds collection.
 */

print('reset:mr_reds[done,champions,champions_data]');

db.mr_reds.update({},
                    {'$unset': {
                                'done': 0,
                                'champions': [],
                                'champions_data': [],
                    }},
                    {'multi': 1});

print('reset:mr_champions[red_posts,rioter_counter,]');

db.mr_champions.update({},
                        {'$unset': {
                                    'rioter_counter': [],
                                    'red_posts': [],
                        }},
                        {'multi':1});