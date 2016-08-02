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

var query = ids.cleanse ? {}:{'name': {'$in': ids.rioters}};

var rioters_bulk = db.mr_rioters.initializeUnorderedBulkOp();

var rioters = db.mr_reds.aggregate([
    { $match: query },
	{ $group: { _id: "$rioter", count: {$sum: 1}, }}
])

var glorious_per_rioter = db.mr_reds.aggregate([
    { $match: { section: { $in: glorious_sections }}},
	{ $group: { _id: "$rioter", count: {$sum: 1}, }},
	{ $out: "glorious_per_rioter" },
])

var champ_per_rioter = db.mr_reds.aggregate([
	{ $group: { _id: { champions: "$champions", rioter: "$rioter"}}},
	{ $unwind: "$_id.champions" },
	{ $group: { _id: { champion: "$_id.champions", rioter: "$_id.rioter"}, count: { $sum: 1} }},
	{ $group: { _id: "$_id.rioter", champions: { $push: { name: "$_id.champion", count: "$count" }}}},
	{ $out: "champ_per_rioter" },
])

var section_per_rioter = db.mr_reds.aggregate([
	{ $group: { _id: { section: "$section", rioter: "$rioter"}, count: { $sum: 1 }}},
	{ $group: { _id: "$_id.rioter", sections: { $push: { section: "$_id.section", count: "$count"}}}},
	{ $out: "section_per_rioter" },
])

rioters.forEach(function(r) {
    var champ = db.champ_per_rioter.findOne({ "_id": r._id })
    if (champ !== null)
    {
        for (i=0;i<champ.champions.length;i++)
        {
            var url_id = urlIDize(champ.champions[i].name)
            champ.champions[i].url_id = url_id
            champ.champions[i].portrait = url_id + ".png"
        }
    }
    var section = db.section_per_rioter.findOne({ "_id": r._id })
    var glorious = db.glorious_per_rioter.findOne({ "_id": r._id })
    var last_post
    var reds = db.mr_reds.find({'rioter': r._id}).sort({'date':-1}).limit(1)
    if (reds.hasNext())
    {
        last_post = reds.next();
    }
    var update = { $set: {
        "name": r._id,
        "total_posts": r.count,
        "glorious_posts": glorious === null ? 0:glorious.count,
        "url_id": urlIDize(r._id),
        "last_post": last_post,
        "champions_occurrences": champ === null ? []:champ.champions,
        "sections_occurrences": section.sections,
    }}
    rioters_bulk.find({ "name": r._id }).upsert().updateOne( update )
});

db.champ_per_rioter.drop()
db.section_per_rioter.drop()
db.glorious_per_rioter.drop()

rioters_bulk.execute();

print("gen:index")
db.mr_rioters.createIndex( { 'name': "text", 'posts': "text"} );
