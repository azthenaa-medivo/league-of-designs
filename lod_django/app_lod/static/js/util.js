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