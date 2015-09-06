/*
 *  League of Designs Postimport v1.1.
 *  Now checks if we haven't filled the Champions field (hue) beforehand to save us some time (up to thrice as fast !).
 *  By Artemys, m'lord humble butler.
 *  Looks for the champion's name in the Thread title and Post contents. It's that simple !
 */

print('postimport:lod');

db.mr_champions.find().forEach(function(champion_res) {
    var rioter_counter = {};
    db.mr_reds.find({'$text': {'$search': champion_res['search']}, 'champions': {'$not': {'$in': [champion_res['name']]}},},
                    {'post_id': 1, 'rioter': 1, 'url': 1, 'contents': 1, 'date': 1, 'thread': 1}).forEach(
                        function(red){
                            // Update champion data if it's not already done.
                            op_r = db.mr_reds.update({'_id': red['_id'],},
                                {
                                    '$push': {
                                            'champions_data': {
                                                'name': champion_res['name'],
                                                'url_id': champion_res['url_id'],
                                                'portrait': champion_res['portrait'],
                                                'search': champion_res['search'],
                                            },
                                            'champions': champion_res['name']
                                    },
                            });
                            // Taking care of the champions now.
                            update = {
                                        'post_id': red['post_id'],
                                        'rioter': red['rioter'],
                                        'url': red['url'],
                                        'contents': red['contents'],
                                        'date': red['date'],
                                        'thread': red['thread'],
                            };
                            op_c = db.mr_champions.update(
                            {'_id': champion_res['_id'], 'red_posts.post_id': red['post_id']},
                            {
                                '$set': {
                                    'red_posts.$': update
                                }
                            });
                            // If no champion was modified then we can safely push.
                            if (op_c.nMatched === 0) {
                                db.mr_champions.update({'_id': champion_res['_id']},
                                    {
                                        '$push': {
                                            'red_posts': update
                                        }
                                    }
                                );
                            }
                            // Update Rioter Counters DOTA2 SPECIALIZATION ZOMG GC YOU ARE BAD wowsoTILT
                            if (red['rioter'] in rioter_counter)
                            {
                                rioter_counter[red['rioter']]['count'] += 1;
                            } else {
                                rioter_counter[red['rioter']] = {};
                                rioter_counter[red['rioter']]['count'] = 1;
                                rioter_counter[red['rioter']]['name'] = red['rioter'];
                            }
                        });
    update_rioter_counter = [];
    for (r in rioter_counter)
    {
        update_rioter_counter.push(rioter_counter[r]);
    }
    db.mr_champions.update({'_id': champion_res['_id']}, {$set: {'rioter_counter': update_rioter_counter}});
});