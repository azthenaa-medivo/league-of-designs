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
    $(document).ready(function() {
        var champNav = $('#champions-navbar').DataTable({
            "order": [[ 2, "desc" ]],
            "info": false,
            "lengthMenu": [[1], [1]],
            "dom": 'rt<"clear">',
            "order": [[ 1, "asc" ]],
            "language": {
                "search": "Search:",
                "zeroRecords": "Wait, <i>WHO</i> ?"
            },
            "columnDefs": [
            {
                "targets": [ 3, 4 ],
                "visible": false,
            },]
        });
        // Search Enter Key
        $('#champion-navbar-search').unbind();
        $('#champion-navbar-search').bind('keyup', function(e) {
            if ($(this).val() === '')
            {
                $('#champions-navbar').addClass('hidden');
                return;
            }
            if (e.keyCode == 13) {
                rowData = champNav.row(0, {row: 'current', search: 'applied'}).data();
                window.open(rowData[3], '_self');
            }
            $('#champions-navbar').removeClass('hidden');
            champNav.column(4).search($(this).val()).draw();
        });
        // Hide everything if out of focus.
        $('#champion-navbar-search input').focusout(function() {
            // Minor timeout to allow redirection.
            setTimeout(function() {
                    $('#champions-navbar').addClass('hidden');
                }, 100);
        });
        $('#champion-navbar-search input').focus(function() {
            if ($('#champion-navbar-search input').val() !== '')
            {
                $('#champions-navbar').removeClass('hidden');
            }
        });
    });

    // Binding table row links
    $('tr[data-href]').on("click", function() {
        window.open($(this).data('href'), '_self');
    });

    // Filters options
    $(document).ready(function() {
        $('label').click(function() {
            $('input[value='+$(this).attr('for')+']').click();
        });
    });

    // Timeout messages
    setTimeout(function() { $('#messagesDiv').animate({'height':'0px'}, function() { $('#messagesDiv').hide() } );}, 5000);

    // Pretty tables
    $("tr").hover(function() {
        $(this).animate({'background-color': 'rgba(230,255,230,1)'});
    }, function() {
        $(this).animate({'background-color': 'white'});
    });

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
