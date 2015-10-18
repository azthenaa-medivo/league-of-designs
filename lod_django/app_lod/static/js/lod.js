/*
 *  LoD Javascript ! Includes every function required for base.html.
 */

 $(document).ready(function() {
    // Back to top button
    // Only enable if the document has a long scroll bar
    // Note the window height + offset
    if ( ($(window).height() + 100) < $(document).height() ) {
        $('#top-link-block').removeClass('hidden').affix({
            offset: {top:100}
        });
    }

    // Navbar search tool
    var template_champion_portrait = Handlebars.compile($("#handlebars-champion-portrait").html());
    var template_champion_red_posts_count = Handlebars.compile($("#handlebars-champion-red-posts-count").html());
    var template_champion_url = Handlebars.compile($("#handlebars-champion-url").html());
    var template_champion_search = Handlebars.compile($("#handlebars-champion-search").html());
    $(document).ready(function() {
        var champNav = $('#champions-navbar').DataTable({
            "ajax": {
                "url": "/champions",
                "type": "GET",
                "data": function ( args ) {
                            projection = {'projection': {'portrait':1, 'name':1, 'glorious_posts':1, 'total_posts':1, 'search':1, 'url_id':1}};
                            return {"args": JSON.stringify( $.extend(args, projection))};
                        },
            },
            "order": [[ 2, "desc" ]],
            "lengthMenu": [[1], [1]],
            "dom": 'rt<"clear">',
            "language": {
                "search": "Search:",
                "zeroRecords": "Wait, <i>WHO</i> ?"
            },
            "columns": [
                    { "render": function( data, type, full, meta ) {
                        return template_champion_portrait(full);
                    }},
                    { "data": "name" },
                    { "render": function( data, type, full, meta ) {
                        return template_champion_red_posts_count(full);
                    }},
                    { "render": function( data, type, full, meta ) {
                        return template_champion_url(full);
                    }},
                    { "render": function( data, type, full, meta ) {
                        return template_champion_search(full);
                    }},
                ],
            "columnDefs": [
            {
                "targets": [ 3, 4 ],
                "visible": false,
            },],
        });
        // Search Enter Key
        $('#css-nav-search').submit(function(e) {
            e.preventDefault();
            return false;
        });
        $('#champion-navbar-search').unbind();
        $('#champion-navbar-search').bind('keyup', function(e) {
            if ($(this).val() === '')
            {
                $('#champions-navbar').addClass('hidden');
                return;
            }
            if (e.keyCode == 13) {
                rowData = champNav.row(0, {row: 'current', search: 'applied'}).data();
                window.open(rowData['DT_RowAttr']['data-href'], '_self');
            }
            $('#champions-navbar').removeClass('hidden');
            champNav.column(4).search($(this).val()).draw();
        });
        // Hide everything if out of focus.
        $('#champion-navbar-search').focusout(function() {
            // Minor timeout to allow redirection.
            setTimeout(function() {
                    $('#champions-navbar').addClass('hidden');
                }, 100);
        });
        $('#champion-navbar-search').focus(function() {
            if ($('#champion-navbar-search').val() !== '')
            {
                $('#champions-navbar').removeClass('hidden');
            }
        });
    });

    // Filters options
    $(document).ready(function() {
        $('label').click(function() {
            $('input[value='+$(this).attr('for')+']').click();
        });
    });

    // Timeout messages
    setTimeout(function() { $('#messagesDiv').animate({'height':'0px'}, function() { $('#messagesDiv').hide() } );}, 5000);

    $("th").hover(function() {
        $(this).animate({'background-color': 'rgba(128,0,0,1)', 'color':'white'});
    }, function() {
        $(this).animate({'background-color': 'rgba(255,255,255,1)', 'color':'black'});
    });

    // Ago function (+ interval wowsoSPOOKY)
    function agoStuff() {
        var now = new Date();
        $('.computed-date').each(function() {
            var then = new Date($(this).attr('data-date'));
            $(this).text(ago(now - then));
            $(this).parent('td').attr('data-order', now-then);
        });
    }
    agoStuff();
    setInterval(agoStuff, 1000);

    // Pretty stuff below
    $('img.round-portrait').hover(function() {
            $(this).animate({'border-color': 'red'});
        }, function() {
            $(this).animate({'border-color': 'black'});
    });
});
