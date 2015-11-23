/*
 *  Version 1.6 : R E W O R K
 */

// Load config : red posts to treat.
var ids = db.config.findOne({'name': 'last_batch'});
print('postimport:rioters');
if (!(ids.has_work))
{
    print('No new Red Post to treat !');
    quit();
}

load('utils.js');

var rioters_bulk = db.mr_rioters.initializeUnorderedBulkOp();
var query = ids.cleanse ? {}:{'name': {'$in': ids.rioters}};

db.mr_rioters.find(query).forEach(function(rioter) {
    // Just count() stuff !
    var glorious_posts = db.mr_reds.find({'rioter': rioter['name'], 'is_glorious': true}).count();
    var total_posts = db.mr_reds.find({'rioter': rioter['name']}).count();
    // We are sure to have at least 1 so index 0 always exists.
    var latest = db.mr_reds.find({'rioter': rioter['name']}).sort({'date':-1})[0];
    // Now let's count champions !
    var champion_occurrences = [];
    db.mr_champions.find().forEach(function(champ) {
        // Could be faster by using an incremental way to do stuff but FOR NOW THIS WILL DO
        var count = db.mr_reds.find({'champions': {'$in': [champ['name']]}, 'rioter': rioter['name']}).count();
        if (count > 0)
        {
            champion_occurrences.push({ 'count': count,
                                        'name': champ['name'],
                                        'url_id': champ['url_id'],
                                        'portrait': champ['portrait'],
                                        'search': champ['search']});
        }
    });
    rioters_bulk.find({'_id': rioter['_id']}).updateOne({$set: {
                                                            'last_post': latest,
                                                            'champion_occurrences': champion_occurrences,
                                                            'glorious_posts': glorious_posts,
                                                            'total_posts': total_posts,
    }});
});

rioters_bulk.execute();
db.mr_rioters.createIndex( { 'name': "text", 'posts': "text"} );