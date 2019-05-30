print('load:utils.js');

var glorious_sections = ["Gameplay", "Dev Corner", "Gameplay & Balance", "Champions & Gameplay", "Maps & Modes",
                            "Live Gameplay Balance", "Champions & Gameplay Feedback", "Story & Art", "Story, Art, & Sound",
                            "Sound & Music", "General PBE Feedback"];
var tags = ["rework", "buff", "nerf"];

function urlIDize(text) {
    return text.replace(/\W/g, '');
}

function contains(array, value) {
    for (var p=0;p<array.length;p++)
    {
        if (array[p] === value)
        {
            return true;
        }
    }
    return false;
}

function getElementMatching(array, field, value)
{
    if (array === undefined)
    {
        return null;
    }
    for(var l;l<array.length;l++)
    {
        if (array[l][field] === value)
        {
            return array[l];
        }
    }
    return null;
}

function capitalize(s)
{
    return s[0].toUpperCase() + s.slice(1);
}

// Super Global Variables

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
    'Kai\'Sa': 'kaisa',
    'Karthus': '',
    'Kassadin': 'kass',
    'Katarina': 'kata',
    'Kayle': '',
    'Kayn': 'rhaast',
    'Kindred': 'lamb wolf',
    'Kha\'Zix': 'kha zix kz',
    'Kled': 'skaarl holyshit',
    'Kog\'Maw': 'kog maw',
    'LeBlanc': 'lb',
    'Leona': 'leo',
    'Lissandra': 'liss',
    'Lucian': 'losian cull',
    'Lux': 'funklen',
    'Maokai': 'ayyy lemao mao',
    'Master Yi': '"master" "yi"',
    'Mordekaiser': 'morde kaiser',
    'Morgana': 'morg',
    'Nasus': 'doge',
    'Nautilus': 'naut',
    'Nidalee': 'nida nid',
    'Nocturne': 'noc',
    'Olaf': '',
    'Ornn': '',
    'Pantheon': 'panth',
    'Quinn': 'valor squak',
    'Rek\'Sai': 'rek sai',
    'Renekton': 'renek',
    'Riven': 'OPSHIT',
    'Sejuani': 'seju',
    'Shyvana': 'shyv',
    'Sona': '',
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
    'Xayah': '',
    'Yorick': ''
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
    "Camille": "piltover",
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
    "Kai'Sa": "void",
    "Kalista": "shadow-isles",
    "Karma": "ionia",
    "Karthus": "shadow-isles",
    "Kassadin": "void",
    "Katarina": "noxus",
    "Kayle": "targon",
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
    "Morgana": "targon",
    "Nasus": "shurima",
    "Nocturne": "shadow-isles",
    "Nunu": "freljord",
    "Olaf": "freljord",
    "Orianna": "piltover",
    "Ornn": "freljord",
    "Pantheon": "targon",
    "Poppy": "demacia",
    "Pyke": "bilgewater",
    "Quinn": "demacia",
    "Rakan": "ionia",
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
    "Urgot": "piltover",
    "Varus": "ionia",
    "Vayne": "demacia",
    "Vel'Koz": "void",
    "Vi": "piltover",
    "Viktor": "zaun",
    "Vladimir": "noxus",
    "Volibear": "freljord",
    "Warwick": "zaun",
    "Wukong": "ionia",
    "Xayah": "ionia",
    "Xerath": "shurima",
    "Xin Zhao": "demacia",
    "Yasuo": "ionia",
    "Yorick": "shadow-isles",
    "Zac": "zaun",
    "Zed": "ionia",
    "Ziggs": "piltover",
    "Zilean": "shurima",
    "Zoe": "targon",
    "Zyra": "shadow-isles",
};
