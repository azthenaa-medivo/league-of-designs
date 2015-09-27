/*
 *  League of Designs Postimport v1.1.
 *  Now checks if we haven't filled the Champions field (hue) beforehand to save us some time (up to thrice as fast !).
 *  By Artemys, m'lord humble butler.
 *  Looks for the champion's name in the Thread title and Post contents. It's that simple !
 */

load('utils.js');

print('postimport:lod');

db.mr_champions.find().forEach(function(champion_res) {
    var rioter_counter = {};
    var glorious = champion_res['glorious_posts'];
    var total = champion_res['total_posts'];
    db.mr_reds.find({'$text': {'$search': champion_res['search']},
                        'champions': {'$not': {'$in': [champion_res['name']]}}}).forEach(
                        function(red){
                            // Update champion data if it's not already done.
                            // Check the tags
                            var new_tags = [];
                            var up_op_r = {'$push': {
                                            'champions_data': {
                                                'name': champion_res['name'],
                                                'url_id': champion_res['url_id'],
                                                'portrait': champion_res['portrait'],
                                                'search': champion_res['search'],
                                            },
                                            'champions': champion_res['name'],
                            },};
                            for (var t=0;t<champion_res['tags'].length;t++)
                            {
                                if (!(contains(new_tags, champion_res['tags'][t])))
                                {
                                    new_tags.push(champion_res['tags'][t]);
                                }
                            }
                            up_op_r['$push']['tags'] = {'$each': new_tags};
                            op_r = db.mr_reds.update({'_id': red['_id'],}, up_op_r);
                            // Taking care of the champions now.
                            update = {
                                        'post_id': red['post_id'],
                                        'rioter': red['rioter'],
                                        'url': red['url'],
                                        'contents': red['contents'],
                                        'date': red['date'],
                                        'thread': red['thread'],
                                        'section': red['section'],
                                        'region': red['region'],
                                        'is_glorious': red['is_glorious'],
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

                            // Update posts number ! wowsoLOD1.2
                            if (contains(glorious_sections, red['section']))
                            {
                                glorious++;
                            }
                            total++;
                        });
    var update_rioter_counter = champion_res['rioter_counter'] === undefined ? []:champion_res['rioter_counter'];
    for (var r in rioter_counter)
    {
        var current = getElementMatching(update_rioter_counter, 'name', r);
        if (current != null)
        {
            // If it exists we had the points
            current['count'] += rioter_counter['count'];
            update_rioter_counter.push(current);
        } else {
            // If it doesn't exist it's the start of a new journey
            update_rioter_counter.push(rioter_counter[r]);
        }
    }
    db.mr_champions.update({'_id': champion_res['_id']}, {$set: {'rioter_counter': update_rioter_counter,
                                                                 'total_posts': total,
                                                                 'glorious_posts': glorious}});
});