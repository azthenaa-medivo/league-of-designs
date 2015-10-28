/*
*   Some cool functions
*/

function ago(time) {
    /*
     *  Computes time and tells you how long ago it was. Months have 30 days because I decided so.
     */
    if (time < 1000) {
        return 'just now';
    }
    // SPECIAL CASE
    if (time < 10000) {
        return 'a few seconds ago';
    }
    // Seconds
    if (time < 60000) {
        return Math.floor(time/1000) + ' seconds ago'
    }
    // Minutes
    if (time < 3600000) {
        n = Math.floor(time/60000);
        return n + ' minute'+plural(n)+' ago';
    }
    // Hours
    if (time < 86400000) {
        n = Math.floor(time/3600000);
        return n + ' hour'+plural(n)+' ago';
    }
    // Days
    if (time < 2592000000) {
        n = Math.floor(time/86400000);
        return n + ' day'+plural(n)+' ago';
    }
    // Months
    if (time < 31104000000) {
        n = Math.floor(time/2592000000);
        return n + ' month'+plural(n)+' ago';
    }
    // Years
    if (time > 31104000000) {
        n = Math.floor(time/31104000000);
        return n + ' year'+plural(n)+' ago';
    }
}

function plural(number) {
    // Return 's' if there number is several. Y'know.
    if (number >= -1 && number <= 1)
    {
        return '';
    } else {
        return 's';
    }
}

function generateRGBAColor(opacity)
{
    if (opacity === undefined)
    {
        opacity = 1;
    }
    res = 'rgba(';
    for (j=0;j<3;j++)
    {
        res += Math.floor(Math.random()*255)+',';
    }
    return res+opacity+')';
}

/*
*	Return a random hexadecimal color starting with #, like #4fa5cd.
*	I had my own but this one's neater.
*/
function generateHexColor()
{
	return '#'+(Math.random()*0xFFFFFF<<0).toString(16);
}

function capitalize(s)
{
    return s[0].toUpperCase() + s.slice(1);
}

// Buttonize Django CheckboxSelectMultiple Forms. param:element is expected to be a function (anonymous ?)
function buttonize(selector, element, what_class, add_class) {
    $(selector).each(function() {
        $(this).parent().first().addClass('hidden');
        $(this).parent().parent().first().append(element($(this)));
        if (add_class != undefined && what_class != undefined)
        {
            $(what_class).addClass(add_class);
        }
    });
}

// USE UNDERSCORE.JS FOOL
function union_arrays (x, y) {
  var obj = {};
  for (var i = x.length-1; i >= 0; -- i)
     obj[x[i]] = x[i];
  for (var i = y.length-1; i >= 0; -- i)
     obj[y[i]] = y[i];
  var res = []
  for (var k in obj) {
    if (obj.hasOwnProperty(k))  // <-- optional
      res.push(obj[k]);
  }
  return res;
}