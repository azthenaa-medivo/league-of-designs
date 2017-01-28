// Load config : red posts to treat.
var ids = db.config.findOne({'name': 'last_batch'});
print('postimport:red-posts');
if (!(ids.has_work))
{
    print('No new Red Post to treat !');
    quit();
}

load('utils.js');

var bulk = db.mr_reds.initializeUnorderedBulkOp();
var query = ids.cleanse ? {}:{'post_id': {'$in': ids.post_ids}};

var red_updates = 0;

db.reds.find(query).forEach(function(res) {
    // If it's a self-post (not a reply), there's no 'comment' field.

    red_updates = red_updates + 1;

    var post_id, post_url, post_section, post_thread, digInto;
    if (res['comment'] === undefined)
    {
        post_url = 'http://boards.'+res['region']+'.leagueoflegends.com/en/c/' +
                res['discussion']['application']['shortName']+'/'+res['discussion']['id'];
        post_section = res['discussion']['application']['name'];
        post_thread = res['discussion']['title'];
        post_thread_id = res['discussion']['id'];
        digInto = res['discussion'];
    } else {
        post_url = 'http://boards.'+res['region']+'.leagueoflegends.com/en/c/' +
                res['comment']['discussion']['application']['shortName']+'/'+res['comment']['discussion']['id'] +
                '?comment='+res['comment']['id'];
        post_section = res['comment']['discussion']['application']['name'];
        post_thread = res['comment']['discussion']['title'];
        post_thread_id = res['comment']['discussion']['id'];
        digInto = res['comment'];
    }
    var new_post = {
        'post_id': res['post_id'],
        'url': post_url,
        'rioter': digInto['user']['name'],
        'rioter_url_id': urlIDize(digInto['user']['name']),
        'region': res['region'].toUpperCase(),
        'date': new Date(digInto['createdAt']),
        'contents': digInto['message'],
        'thread': post_thread,
        'thread_id': post_thread_id,
        'section': post_section,
        'is_glorious': contains(glorious_sections, post_section),
        'tags': [],
        'champions': [],
        'champions_data': [],
    }
    var parent = digInto['parentComment'];
    if (parent != undefined)
    {
        new_post['parent'] = {
            'post_id': post_thread_id + ',' + parent['id'],
            'post_url': post_url.split('?')[0] + '?comment='+parent['id'],
            'contents': parent['message'],
            'user': parent['user']['name'],
            'date': new Date(parent['createdAt']),
        };
        new_post['has_parent'] = true;
    }
    // Check for tags !
    for (i=0;i<tags.length;i++)
    {
        var regexTest = new RegExp(tags[i], "gi");
        if (regexTest.test(new_post['contents']) || regexTest.test(new_post['thread']))
        {
           new_post['tags'].push(tags[i]);
        }
    }
    bulk.find({'post_id': res['post_id']}).upsert().update({'$set': new_post});
});

print("Red Updates : " + red_updates)

bulk.execute();
db.mr_reds.createIndex( { 'thread': "text", 'contents' : "text" } );
