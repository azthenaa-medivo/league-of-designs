/*
 *  Version 1.2 : Now adds the number of posts to stuff
 */

load('utils.js');

print('postimport:rioters');

db.mr_reds.find({'done': {'$ne': 1}}).forEach(function(red) {
    // Now we map that to Rioters <3
    // First we check if the Rioter exists, and if needed create it.
    db.mr_rioters.update({'name': red['rioter']}, {'$set': {'name': red['rioter'], 'url_id': urlIDize(red['rioter'])}}, {upsert: true});
    op_rioters = db.mr_rioters.update(
        {'name': red['rioter'], 'posts.post_id': red['post_id']},
        {
            '$set': {
                'posts.$': red
            }
    });
    // If no rioter's red posts was modified then we can safely push.
    if (op_rioters.nMatched === 0) {
        db.mr_rioters.update({'name': red['rioter']},
            {
                '$push': {
                    'posts': red
                }
            }
        );
    }
});

db.mr_reds.update({'done': {'$ne': 1}}, {'$set':{'done':1}}, {'multi': 1});

// And now we check the different champions they talked about.

var rioters_bulk = db.mr_rioters.initializeUnorderedBulkOp();

db.mr_rioters.find().forEach(function(rioter) {
    var champ_occ = {}; // 8/8 would name a variable again
    var glorious_posts = 0;
    var total_posts = rioter['posts'].length;
    for (i=0;i<rioter['posts'].length;i++)
    {
        if ('champions' in rioter.posts[i])
        {
            for (j=0;j<rioter['posts'][i]['champions_data'].length;j++)
            {
                if (!(rioter['posts'][i]['champions_data'][j]['name'] in champ_occ))
                {
                    champ_occ[rioter['posts'][i]['champions_data'][j]['name']] = rioter['posts'][i]['champions_data'][j];
                    champ_occ[rioter['posts'][i]['champions_data'][j]['name']]['count'] = 1;
                } else {
                    champ_occ[rioter['posts'][i]['champions_data'][j]['name']]['count'] += 1;
                }
            }
        }
        if (contains(glorious_sections, rioter['posts'][i]['section']))
        {
            glorious_posts += 1;
        }
    }
    update = [];
    for (k in champ_occ)
    {
        update.push(champ_occ[k]);
    }
    rioters_bulk.find({'_id': rioter['_id']}).update({$set: {
                                                                'champion_occurrences': update,
                                                                'glorious_posts': glorious_posts,
                                                                'total_posts': total_posts,
                                                            }});
});

rioters_bulk.execute();