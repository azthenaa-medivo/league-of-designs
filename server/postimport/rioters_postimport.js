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
var rioters_array = [];

// So I male 3*N_rioters + N_champions queries here (no reading !). I can probably do better, though it'll do for now.
db.mr_rioters.find(query).forEach(function(rioter) {
    // Just count() stuff !
    var glorious_posts = db.mr_reds.find({'rioter': rioter.name, 'is_glorious': true}).count();
    var total_posts = db.mr_reds.find({'rioter': rioter.name}).count();
    // We are sure to have at least 1 so index 0 always exists.
    var latest = db.mr_reds.find({'rioter': rioter.name}).sort({'date': -1}).limit(1)[0];
    rioters_array.push({'_id': rioter._id, 'name': rioter.name, 'data': {
            'last_post': latest,
            'glorious_posts': glorious_posts,
            'total_posts': total_posts,
            'champions_occurrences': [],
    }});
});

db.mr_champions.find().forEach(function(champ) {
    if ('rioter_counter' in champ)
    {
        for (var i=0;i<champ.rioter_counter.length;i++)
        {
            for (var j=0;j<rioters_array.length;j++)
            {
                if (rioters_array[j].name === champ.rioter_counter[i].name)
                {
                    rioters_array[j].data.champions_occurrences.push({
                        'count': champ.rioter_counter[i].count,
                        'name': champ.name,
                        'url_id': champ.url_id,
                        'portrait': champ.portrait,
                        'search': champ.search,
                    });
                }
            }
        }
    }
});

for (var k=0;k<rioters_array.length;k++)
{
    rioters_bulk.find({'_id': rioters_array[k]['_id']}).updateOne({$set: rioters_array[k]['data']});
}
rioters_bulk.execute();
db.mr_rioters.createIndex( { 'name': "text", 'posts': "text"} );