/*
 *  League of Designs Postimport v1.6.
 *  ---
 *  Now does only required Red Posts (could even go faster, but later) and use $addToSet because it's A W E S O M E
 *  Also no longer stores Red Posts in Champions documents. Who cares we're using this MY WAY.
 *  ---
 *  By Artemys, m'lord humble butler.
 *  Looks for the champion's name in the Thread title and Post contents. It's that simple !
 */

// Load config : red posts to treat.
var ids = db.config.findOne({'name': 'last_batch'});
print('postimport:lod');
if (!(ids.has_work))
{
    print('No new Red Post to treat !');
    quit();
}

load('utils.js');
var mr_reds_bulk = db.mr_reds.initializeUnorderedBulkOp();
var mr_champions_bulk = db.mr_champions.initializeUnorderedBulkOp();

db.mr_champions.find().forEach(function(champion_res) {
    var rioter_counter = {};
    var glorious = champion_res['glorious_posts'];
    var total = champion_res['total_posts'];
    var query = ids.cleanse ? {
                        '$text': {'$search': champion_res['search']},
                        'champions': {'$not': {'$in': [champion_res['name']]}}}:
                        {'post_id': {'$in': ids.post_ids}, '$text': {'$search': champion_res['search']},
                        'champions': {'$not': {'$in': [champion_res['name']]}}};
    db.mr_reds.find(query).forEach(
                        function(red){
                            var new_tags = [];
                            var red_update = {'$push': {
                                                'champions_data': {
                                                    'name': champion_res['name'],
                                                    'url_id': champion_res['url_id'],
                                                    'portrait': champion_res['portrait'],
                                                    'search': champion_res['search'],
                                                },
                                                'champions': champion_res['name'],
                            }, '$addToSet': {}};
                            red_update['$addToSet']['tags'] = {'$each': champion_res['tags']};
                            mr_reds_bulk.find({'_id': red['_id'],}).update(red_update);
                            // Update Rioter Counters DOTA2 SPECIALIZATION ZOMG GC YOU ARE BAD wowsoTILT
                            if (red['rioter'] in rioter_counter)
                            {
                                rioter_counter[red['rioter']]['count'] += 1;
                            } else {
                                rioter_counter[red['rioter']] = {};
                                rioter_counter[red['rioter']]['count'] = 1;
                                rioter_counter[red['rioter']]['name'] = red['rioter'];
                                rioter_counter[red['rioter']]['url_id'] = red['rioter_url_id'];
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
            // If it doesn't exist it's the start of a new journey EVERY STEP
            update_rioter_counter.push(rioter_counter[r]);
        }
    }
    mr_champions_bulk.find({'_id': champion_res['_id']}).update({'$set': {
                                                                         'rioter_counter': update_rioter_counter,
                                                                         'total_posts': total,
                                                                         'glorious_posts': glorious}});
});

mr_reds_bulk.execute();
mr_champions_bulk.execute();
print('gen:text-index');
db.mr_reds.createIndex( { 'thread': "text", 'contents': "text", 'rioter': "text", 'champions': "text", 'tags': "text" } );
