print('load:utils.js');

var glorious_sections = ["Gameplay & Balance", "Champions & Gameplay", "Maps & Modes", "Champions & Gameplay Feedback"];

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