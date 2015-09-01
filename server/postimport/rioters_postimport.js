print('postimport:rioters');

db.mr_reds.find().forEach(function(red) {
    // Now we map that to Rioters <3
    // First we check if the Rioter exists, and if needed create it.
    db.mr_rioters.update({'name': red['rioter']}, {'$set': {'name': red['rioter']}}, {upsert: true});
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

// And now we check the different champions they talked about.

db.mr_rioters.find().forEach(function(rioter) {
    champ_occ = {}; // 8/8 would name a variable again
    champ_counter = 0;
    for (i=0;i<rioter.posts.length;i++)
    {
        if ('champions' in rioter.posts[i])
        {
            for (j=0;j<rioter.posts[i].champions_data.length;j++)
            {
                if (!(rioter.posts[i].champions_data[j]['name'] in champ_occ))
                {
                    champ_occ[rioter.posts[i].champions_data[j]['name']] = rioter.posts[i].champions_data[j];
                    champ_occ[rioter.posts[i].champions_data[j]['name']]['count'] = 1;
                } else {
                    champ_occ[rioter.posts[i].champions_data[j]['name']]['count'] += 1;
                }
            }
            champ_counter += 1;
        }
    }
    update = [];
    for (k in champ_occ)
    {
        update.push(champ_occ[k]);
    }
    db.mr_rioters.update({'_id': rioter['_id']}, {$set: {'champion_occurrences': update, 'champions_posts_counter': champ_counter}});
});