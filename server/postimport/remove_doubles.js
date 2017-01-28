var n_duplicates = 0;

db.reds.aggregate([
	{"$group" : { "_id": "$post_id", "count": { "$sum": 1 }, dups: { "$addToSet": "$_id" }, } },
	{"$match": {"_id" :{ "$ne" : null } , "count" : {"$gt": 1} } },
]).forEach(function(doc) {
	n_duplicates = n_duplicates + 1;
    doc.dups.shift();      // First element skipped for deleting
    db.reds.remove({_id : {$in: doc.dups }});  // Delete remaining duplicates
})

print("Removed : " + n_duplicates)
