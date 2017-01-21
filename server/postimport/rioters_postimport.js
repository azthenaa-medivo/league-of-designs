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

var query = ids.cleanse ? {}:{'rioter': {'$in': ids.rioters}};

var rioters_bulk = db.mr_rioters.initializeUnorderedBulkOp();

// Aggregates the Red Posts by Rioter and count total_posts.
// Result : List of Rioters with total_posts count in "count".
var rioters = db.mr_reds.aggregate([
    { $match: query },
	{ $group: { _id: "$rioter", count: {$sum: 1} } }
]);

var glorious_query = ids.cleanse ? {section: { $in: glorious_sections }}:{ section: { $in: glorious_sections }, rioter: {$in: ids.rioters}}

// Aggregates the Red Posts by Rioter and count glorious_posts.
// Result : List of Rioters with glorious_posts count in "count".
var glorious_per_rioter = db.mr_reds.aggregate([
    { $match: glorious_query },
	{ $group: { _id: "$rioter", count: {$sum: 1}, }},
	{ $out: "glorious_per_rioter" },
])

var query_champ = ids.cleanse ? {}:{'rioter_counter.name': {'$in': ids.rioters}};

// Aggregates the number of champion occurrences for each Rioter.
// Out : List of Rioters and Champions occurrences (champion + times quoted).
var champ_per_rioter = db.mr_champions.aggregate([
	{ $project : { "rioter_counter": 1, "name": 1, "url_id": 1, "portrait": 1 } },
	{ $match : query_champ },
	{ $unwind : "$rioter_counter" },
	{ $sort: {"rioter_counter" : -1, "name": 1}},
	{ $group : { _id : "$rioter_counter.name",
	    champions_occurrences : { $push : { count: "$rioter_counter.count", name: "$name", url_id: "$url_id", portrait: "$portrait" } } } },
	{ $out: "champ_per_rioter" }
])

// Aggregates the number of Section occurrences for each Rioter.
// Out : List of Rioters and Sections occurrences.
var section_per_rioter = db.mr_reds.aggregate([
    { $match : query },
	{ $group: { _id: { section: "$section", rioter: "$rioter"}, count: { $sum: 1 }}},
	{ $group: { _id: "$_id.rioter", sections: { $push: { section: "$_id.section", count: "$count"}}}},
	{ $out: "section_per_rioter" },
])

var i = 0;

rioters.forEach(function(r) {
    i = i + 1
//    print("\n=======\n"+r._id+"\n=======\n")
    var champ = db.champ_per_rioter.findOne({ "_id": r._id })
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
        "champions_occurrences": champ === null ? []:champ.champions_occurrences,
        "sections_occurrences": section.sections,
    }}
    rioters_bulk.find({ "name": r._id }).upsert().updateOne( update )
});

print("Updated " + i + " Rioters.")

rioters_bulk.execute();

print("gen:index")
db.mr_rioters.createIndex( { 'name': "text", 'posts': "text" } );

db.champ_per_rioter.drop();
db.section_per_rioter.drop();
db.glorious_per_rioter.drop();
