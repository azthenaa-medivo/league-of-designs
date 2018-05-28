load('utils.js');

function generateSearchString(text) {
    // Produces a string used to search with CSS selectors !
    var s = text.split(/['\s]/g);
    if (s.length != 1)
    {
        init = buildInitials(s);
        if (init != false)
        {
            text = text + ' ' + init;
        }
    }
    text = text.replace(cleanse_regex, '').trim().replace(/\s+/g, ' ');
    return text;
}

function buildInitials(textArray) {
    var initials = '';
    for (i=0;i<textArray.length;i++)
    {
       initials += textArray[i][0];
    }
    return initials;
}

var bulk = db.mr_champions.initializeUnorderedBulkOp();
print('postimport:champions');

db.champions.find().forEach(function(res) {
    var url_id = urlIDize(res['name']);
    var new_champion = {'$set': {
            'name': res['name'],
            'title': res['title'],
            'lore': res['lore'],
            'portrait': url_id+'.png', // RIOT SANITIZE YOUR POOPOO DATA PLEASE
            'riot_id': res['id'],
            'url_id': url_id,
            'articles': [],
            'total_posts': 0,
            'glorious_posts': 0,
            'home': null,
            'latest_post': null,
        }
    };
    // Resource
    if (url_id in special_champion_resources)
    {
        new_champion['$set']['resource'] = special_champion_resources[url_id];
    } else {
        new_champion['$set']['resource'] = 'Mana';
    }
    // Spells
    var champ_spells = [
        {
            'name': res['passive']['name'],
            'description': res['passive']['description'],
            'image': url_id + 'P.png',
        }
    ];
    var spells_keys = ['Q','W','E','R'];
    for (i=0;i<4;i++)
    {
        var new_spell = {
            'name': res['spells'][i]['name'],
            'description': res['spells'][i]['description'],
        }
        if (res['spells'][i]['altimages'] !== undefined)
        {
            var new_images = [url_id + spells_keys[i] + '0.png'];
            for (j=0;j<res['spells'][i]['altimages'].length;j++)
            {
                new_images.push(url_id + spells_keys[i] + (j+1) + '.png');
            }
            new_spell['image'] = new_images;
            new_spell['is_multi'] = true;
        } else {
            new_spell['image'] = url_id + spells_keys[i] + '.png';
        }
        champ_spells.push(new_spell);
    }
    new_champion['$set']['spells'] = champ_spells;
    // Search strings
    s = generateSearchString(res['name']);
    if (res['name'] in special_champion_names)
    {
        s = s + ' ' + special_champion_names[res['name']];
    }
    new_champion['$set']['search'] = s;
    // ADC tag
    if (contains(res['tags'], 'Marksman'))
    {
        res['tags'].push('ADC');
    }
    new_champion['$set']['tags'] = res['tags'];
    // Location
    if (res["name"] in special_champion_land)
     {
        new_champion["$set"]["home"] = special_champion_land[res["name"]]
     }
    // Init Rioter Counter
    new_champion['$set']['rioter_counter'] = [];
    bulk.find({'name': res['name']}).upsert().updateOne(new_champion);
});

bulk.execute();

db.mr_champions.createIndex( { 'name': "text", 'search': "text" } );
