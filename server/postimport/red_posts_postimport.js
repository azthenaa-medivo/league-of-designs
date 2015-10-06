load('utils.js');

var bulk = db.mr_reds.initializeUnorderedBulkOp();
print('postimport:red-posts');

db.reds.find().forEach(function(res) {
    // If it's a self-post (not a reply), there's no 'comment' field.
    var post_id, post_url, post_section, post_thread, digInto;
    if (res['comment'] === undefined)
    {
        post_url = 'http://boards.'+res['region']+'.leagueoflegends.com/en/c/' +
                res['discussion']['application']['shortName']+'/'+res['discussion']['id'];
        post_section = res['discussion']['application']['name'];
        post_thread = res['discussion']['title'];
        digInto = res['discussion'];
    } else {
        post_url = 'http://boards.'+res['region']+'.leagueoflegends.com/en/c/' +
                res['comment']['discussion']['application']['shortName']+'/'+res['comment']['discussion']['id'] +
                '?comment='+res['comment']['id'];
        post_section = res['comment']['discussion']['application']['name'];
        post_thread = res['comment']['discussion']['title'];
        digInto = res['comment'];
    }
    var new_post = {
        'post_id': res['post_id'],
        'url': post_url,
        'rioter': digInto['user']['name'],
        'region': res['region'].toUpperCase(),
        'date': new Date(digInto['createdAt']),
        'contents': digInto['message'],
        'thread': post_thread,
        'section': post_section,
        'is_glorious': contains(glorious_sections, post_section),
        'tags': [],
    }
    // Check for tags !
    for (i=0;i<tags.length;i++)
    {
        var regexTest = new RegExp("\\b" + tags[i] + "\\b", "gi");
        if (regexTest.test(new_post['contents']) || regexTest.test(new_post['thread']))
        {
           new_post['tags'].push(tags[i]);
        }
    }
    bulk.find({'post_id': res['post_id']}).upsert().update({'$set': new_post});
});

bulk.execute();