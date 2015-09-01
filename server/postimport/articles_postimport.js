var bulk_champions = db.mr_champions.initializeUnorderedBulkOp();
var bulk_articles = db.articles.initializeUnorderedBulkOp();
print('postimport:articles');

db.mr_champions.find().forEach(function(res) {
    var articles = [];
    db.articles.find({'champion': res['_id'].str}).forEach(function(a) {
        var a_up = {'$set': {
            'champion_data': {
                '_id': res['_id'],
                'name': res['name'],
                'url_id': res['url_id'],
                'portrait': res['portrait'],
        }}};
        articles.push({
            'title': a['title'],
            'contents': a['contents'],
            'url_id': a['url_id'],
        });
        bulk_articles.find({'_id': a['_id']}).updateOne(a_up);
    });
    bulk_champions.find({'_id': res['_id']}).updateOne({'$set': {'articles': articles}});
});

bulk_articles.execute();
bulk_champions.execute();