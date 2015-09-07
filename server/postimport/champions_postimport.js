function generateSearchString(text) {
    // Produces a string used to search with CSS selectors !
    var s = text.split(/['\s]/g);
    if (s.length != 1)
    {
        init = buildInitials(s);
        if (init != false)
        {
            return text + ' ' + text.toLowerCase() + ' ' + init;
        }
    }
    return text + ' ' + text.toLowerCase();
}

function buildInitials(textArray) {
    var initials = '';
    for (i=0;i<textArray.length;i++)
    {
       initials += textArray[i][0];
    }
    // Check for words to cleanse
    for (i=0;i<cleanse_words.length;i++)
    {
        if (initials.toLowerCase() === cleanse_words[i])
        {
            return false;
        }
    }
    return initials + ' ' + initials.toLowerCase() + ' ' + initials[0].toUpperCase() + initials[1].toLowerCase();
}

var cleanse_words = ['my',]

var special_champion_names = {
    'Amumu': 'mumu',
    'Blitzcrank': 'bc bitchcrank',
    'Caitlyn': 'Cait cait',
    'Cassiopeia': 'Cass cass',
    'Cho\'Gath': 'nomnomnom',
    'Evelynn': 'Eve eve',
    'Ezreal': 'Ez ez',
    'Fiddlesticks': 'Fiddle fiddle',
    'Gangplank': 'GP gp Gp',
    'Heimerdinger': 'Heimer heimer donger',
    'Jarvan IV': 'j4 J4',
    'Kassadin': 'Kass kass',
    'Katarina': 'Kata kata',
    'LeBlanc': 'lb LB',
    'Leona': 'Leo leo',
    'Lissandra': 'Liss liss',
    'Lucian': 'Losian',
    'Lux': 'finales funklen',
    'Maokai': 'ayyy lemao Mao mao',
    'Mordekaiser': 'morde kaiser #1',
    'Morgana': 'Morg morg',
    'Nasus': 'doge',
    'Nautilus': 'Naut naut',
    'Nidalee': 'Nida nida',
    'Nocturne': 'Noc noc',
    'Pantheon': 'Panth panth',
    'Quinn': 'Valor valor squak',
    'Rammus': 'ok',
    'Renekton': 'Renek renek',
    'Riven': 'OPSHIT',
    'Sejuani': 'Seju seju',
    'Shaco': 'Joker',
    'Shyvana': 'Shyv shyv',
    'Soraka': 'raka',
    'Taric': 'outrageous',
    'Teemo': 'satan 666',
    'Tristana': 'trist Trist',
    'Tryndamere': 'Trynda trynda Tryn trynd',
    'Urgot': 'Urgod urgod',
    'Vladimir': 'Vlad vlad',
    'Volibear': 'Volibro volibro Voli voli',
    'Warwick': 'WW ww',
    'Wukong': 'Wu wu',
}

var special_champion_resources = {
    'Aatrox': 'Health',
    'Akali': 'Energy',
    'DrMundo': 'Health',
    'Garen': 'None',
    'Gnar': 'None',
    'Katarina': 'None',
    'Kennen': 'Energy',
    'LeeSin': 'Energy',
    'Mordekaiser': 'Health',
    'RekSai': 'None',
    'Renekton': 'None',
    'Riven': 'None',
    'Rumble': 'Heat',
    'Shen': 'Energy',
    'Shyvana': 'None',
    'Tryndamere': 'None',
    'Vladimir': 'Health',
    'Yasuo': 'None',
    'Zac': 'Health',
    'Zed': 'Energy',
};

var bulk = db.mr_champions.initializeUnorderedBulkOp();
print('postimport:champions');

db.champions.find().forEach(function(res) {
    var url_id = res['name'].replace(/\W/g, '');
    var new_champion = {'$set': {
            'name': res['name'],
            'title': res['title'],
            'tags': res['tags'],
            'lore': res['lore'],
            'portrait': res['image']['full'],
            'riot_id': res['id'],
            'url_id': url_id,
            'articles': [],
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
    // Init Rioter Counter
    new_champion['$set']['rioter_counter'] = [];
    bulk.find({'name': res['name']}).upsert().updateOne(new_champion);
});

bulk.execute();