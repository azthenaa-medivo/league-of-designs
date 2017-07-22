// Set the last_batch config dates to the last ones found in mr_reds.

var realms = ['NA', 'EUW', 'PBE']
var config = db.config.findOne({'name': 'last_batch'})

for (var i = 0;i<realms.length;i++)
{
    var date = db.mr_reds.find({region: realms[i]}).sort({date: -1}).limit(1)[0]['date']
    config['last_'+realms[i].toLowerCase()] = date
}

db.config.update({'name': 'last_batch'}, {$set: config})