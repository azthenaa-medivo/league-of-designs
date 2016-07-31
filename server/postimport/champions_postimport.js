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

var cleanse_words = ['my', 'miss', 'master', 'dr. '];
var cleanse_regex = new RegExp('\\b('+cleanse_words.join('|')+')\\b', 'gi');

var special_champion_names = {
    'Amumu': 'mumu',
    'Blitzcrank': 'bc bitchcrank',
    'Caitlyn': 'cait',
    'Cassiopeia': 'cass',
    'Cho\'Gath': 'nomnomnom cho gath',
    'Evelynn': '"eve"',
    'Ezreal': 'ez',
    'Gangplank': 'gp',
    'Heimerdinger': 'heimer donger ヽ༼ຈل͜ຈ༽ﾉ',
    'Jarvan IV': 'jarvan j4',
    'Kassadin': 'kass',
    'Katarina': 'kata',
    'Kindred': 'lamb wolf',
    'Kha\'Zix': 'kha zix kz',
    'Kled': 'skaarl holyshit',
    'Kog\'Maw': 'kog maw',
    'LeBlanc': 'lb',
    'Leona': 'leo',
    'Lissandra': 'liss',
    'Lucian': 'losian',
    'Lux': 'funklen',
    'Maokai': 'ayyy lemao mao',
    'Master Yi': '"master" "yi"',
    'Mordekaiser': 'morde kaiser',
    'Morgana': 'morg',
    'Nasus': 'doge',
    'Nautilus': 'naut',
    'Nidalee': 'nida',
    'Nocturne': 'noc',
    'Pantheon': 'panth',
    'Quinn': 'valor squak',
    'Rek\'Sai': 'rek sai',
    'Renekton': 'renek',
    'Riven': 'OPSHIT',
    'Sejuani': 'seju',
    'Shyvana': 'shyv',
    'Soraka': 'raka',
    'Taric': 'outrageous',
    'Teemo': 'satan 666',
    'Tristana': 'trist',
    'Tryndamere': 'trynd',
    'Urgot': 'urgod',
    'Vel\'Koz': 'koz',
    'Vladimir': 'vlad',
    'Volibear': 'volibro voli',
    'Warwick': 'ww',
    'Wukong': 'wu',
}

var special_champion_resources = {
    'Aatrox': 'Health',
    'Akali': 'Energy',
    'DrMundo': 'Health',
    'Garen': 'None',
    'Gnar': 'None',
    'Katarina': 'None',
    'Kennen': 'Energy',
    'Kled': 'Courage',
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

var special_champion_land = {
    "Akali": "ionia",
    "Amumu": "shurima",
    "Anivia": "freljord",
    "Annie": "noxus",
    "Ashe": "freljord",
    "Aurelion Sol": "targon",
    "Azir": "shurima",
    "Blitzcrank": "zaun",
    "Braum": "freljord",
    "Caitlyn": "piltover",
    "Cassiopeia": "noxus",
    "Cho'Gath": "void",
    "Corki": "piltover",
    "Darius": "noxus",
    "Diana": "targon",
    "Dr. Mundo": "zaun",
    "Draven": "noxus",
    "Ekko": "zaun",
    "Elise": "shadow-isles",
    "Evelynn": "shadow-isles",
    "Ezreal": "piltover",
    "Fiddlesticks": "shadow-isles",
    "Fiora": "demacia",
    "Fizz": "bilgewater",
    "Galio": "demacia",
    "Gangplank": "bilgewater",
    "Garen": "demacia",
    "Gragas": "freljord",
    "Graves": "bilgewater",
    "Hecarim": "shadow-isles",
    "Heimerdinger": "piltover",
    "Illaoi": "bilgewater",
    "Irelia": "ionia",
    "Janna": "zaun",
    "Jarvan IV": "demacia",
    "Jayce": "piltover",
    "Jhin": "ionia",
    "Jinx": "piltover",
    "Kalista": "shadow-isles",
    "Karma": "ionia",
    "Karthus": "shadow-isles",
    "Kassadin": "void",
    "Katarina": "noxus",
    "Kennen": "ionia",
    "Kha'Zix": "void",
    "Kled": "noxus",
    "Kog'Maw": "void",
    "LeBlanc": "noxus",
    "Lee Sin": "ionia",
    "Leona": "targon",
    "Lissandra": "freljord",
    "Lucian": "shadow-isles",
    "Lux": "demacia",
    "Malzahar": "void",
    "Maokai": "shadow-isles",
    "Master Yi": "ionia",
    "Miss Fortune": "bilgewater",
    "Mordekaiser": "shadow-isles",
    "Nasus": "shurima",
    "Nocturne": "shadow-isles",
    "Nunu": "freljord",
    "Olaf": "freljord",
    "Orianna": "piltover",
    "Pantheon": "targon",
    "Poppy": "demacia",
    "Quinn": "demacia",
    "Rammus": "shurima",
    "Rek'Sai": "void",
    "Renekton": "shurima",
    "Riven": "noxus",
    "Sejuani": "freljord",
    "Shaco": "noxus",
    "Shen": "ionia",
    "Shyvana": "demacia",
    "Singed": "zaun",
    "Sion": "noxus",
    "Sivir": "shurima",
    "Skarner": "shurima",
    "Sona": "demacia",
    "Swain": "noxus",
    "Syndra": "ionia",
    "Tahm Kench": "bilgewater",
    "Taliyah": "shurima",
    "Talon": "noxus",
    "Taric": "targon",
    "Teemo": "void",
    "Thresh": "shadow-isles",
    "Trundle": "freljord",
    "Tryndamere": "freljord",
    "Twisted Fate": "bilgewater",
    "Twitch": "zaun",
    "Udyr": "freljord",
    "Urgot": "noxus",
    "Varus": "ionia",
    "Vayne": "demacia",
    "Vel'Koz": "void",
    "Vi": "piltover",
    "Viktor": "zaun",
    "Vladimir": "noxus",
    "Volibear": "freljord",
    "Warwick": "zaun",
    "Wukong": "ionia",
    "Xerath": "shurima",
    "Xin Zhao": "demacia",
    "Yasuo": "ionia",
    "Yorick": "shadow-isles",
    "Zac": "zaun",
    "Zed": "ionia",
    "Ziggs": "piltover",
    "Zilean": "shurima",
    "Zyra": "shadow-isles",
};

var bulk = db.mr_champions.initializeUnorderedBulkOp();
print('postimport:champions');

db.champions.find().forEach(function(res) {
    var url_id = urlIDize(res['name']);
    var new_champion = {'$set': {
            'name': res['name'],
            'title': res['title'],
            'lore': res['lore'],
            'portrait': capitalize(url_id.toLowerCase())+'.png', // RIOT SANITIZE YOUR POOPOO DATA PLEASE
            'riot_id': res['id'],
            'url_id': url_id,
            'articles': [],
            'total_posts': 0,
            'glorious_posts': 0,
            'home': null,
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
