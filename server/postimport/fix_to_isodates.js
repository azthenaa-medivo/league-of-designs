// Finds dates that are not in ISODate format and turn them into ISODates. YES !

db.mr_reds.find({'date': {'$not': {'$type': 9}}}).forEach(function(res) {
    var new_date = new Date(res['date']);
    db.mr_reds.update({'_id': res['_id']}, {'date': new_date});
});