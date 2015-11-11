db.mr_reds.find({'thread_id': {'$exists': 0}}).forEach(function(res) {
    if (res['post_id'] != undefined)
    {
        var thread_id = res['post_id'].split(',')[0];
        var re = new RegExp('(^'+thread_id+',|^'+thread_id+'$)');
        db.mr_reds.update({'post_id': {'$regex': re}}, {'$set': {'thread_id': thread_id}}, {'multi': true});
    }
});