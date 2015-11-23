// Normally you don't need this but just in case (for instance after you update to the new API with config control).

db.mr_reds.find().forEach(function(red) {
    var cur = db.mr_reds.find({'post_id': red['post_id']});
    var first = true;
    while (cur.hasNext()) {
        var doc = cur.next();
        if (first) {first = false; continue;}
        db.mr_reds.remove({ _id: doc._id });
    }
});