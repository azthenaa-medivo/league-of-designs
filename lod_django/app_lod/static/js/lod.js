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

    // Ago function
    var now = new Date();
    $('.computed-date').each(function() {
        var then = new Date($(this).attr('data-date'));
        $(this).text(ago(now - then));
        $(this).parent('td').attr('data-order', now-then);
    });
    // Navbar search tool
    $(document).ready(function() {
        var champNav = $('#champions-navbar').DataTable({
            "order": [[ 2, "desc" ]],
            "info": false,
            "lengthMenu": [[1], [1]],
            "dom": '<"top"f>rt<"bottom"><"clear">',
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
        $('#champions-navbar_filter input').unbind();
        $('#champions-navbar_filter input').bind('keyup', function(e) {
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
            champNav.search($(this).val());
            champNav.draw();
        });
        // Hide everything if out of focus.
        $('#champions-navbar_filter input').focusout(function() {
            // Minor timeout to allow redirection.
            setTimeout(function() {
                    $('#champions-navbar').addClass('hidden');
                }, 100);
        });
        $('#champions-navbar_filter input').focus(function() {
            if ($('#champions-navbar_filter input').val() !== '')
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
        $(this).animate({'background-color': 'rgba(0,255,0,0.2)'});
    }, function() {
        $(this).animate({'background-color': 'white'});
    });
 });
