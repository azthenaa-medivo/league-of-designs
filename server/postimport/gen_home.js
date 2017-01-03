// Generate the db.config document that contains data for the Home Page.
// So the Home Page makes ONE query and not 548
load('utils.js');

print("gen:home")

var champs = db.mr_champions.find({}, {'name': 1, 'url_id': 1, 'total_posts': 1, 'glorious_posts': 1, 'portrait': 1, 'search': 1}).sort({"latest_post.date": -1}).limit(8).toArray();
var reds = db.mr_reds.find({'region': {'$in': ['NA', 'PBE']}, 'section' : {'$in': glorious_sections}}).sort({'date': -1}).limit(15).toArray();
var news = db.articles.find({'type': 'News'}).sort({'date_created': -1}).limit(2).toArray();
var rioters = db.mr_rioters.find({}).sort({'last_post.date': -1}).limit(4).toArray();

var home_doc = {'$set': {'name': 'home_page', 'champions': champs, 'reds': reds, 'news': news, 'rioters': rioters}};

db.config.update({'name': 'home_page'}, home_doc, {'upsert': true});
