// `episode' is a global variable that is defined in every .pt file that uses the
// calendar. `episode' currently only takes on the values `standby' and `event'
// as the only views that currently use this calendar code are the Standby and
// Events calendar.
$(function() {
    var dates = [];
    function get_updates() {
        // Get all of the dates for the desired episode type
        var request = $.ajax({
            url: '/dates.json',
            type: 'GET',
            data: {type: episode}
        });
        request.done(function(data) {
            $.each(data, function (key, val) {
                // Add the start date and end date onto the dates array so
                // `highlightDays' knows which dates to highlight.
                dates.push(val[0]);
                dates.push(val[1]);
            });

            // Display the calendar
            $('#datepicker').datepicker({
                // Hilight the days which Episodes occur on
                beforeShowDay: highlightDays,

                // When the user clicks on a date, make an AJAX call to the
                // pyramid server to get all of the episodes occurring on that
                // particular date.
                onSelect: function(date) {
                    // Make an AJAX request back to the pyramid server to get
                    // all of the episodes occurring on this particular date.
                    var request = $.ajax({
                        type: 'GET',
                        url: '/detailed_info.json',
                        data: {date: date, type: episode}
                    });
                    
                    // When the request comes back, empty the section where
                    // episodes are displayed and populate it with all of the
                    // episodes occurring on this date.
                    request.done(function(msg) {
                        if (episode == 'standby') {
                            $('#standbys').empty();
                            $('#standbys').append('<br />');
                            $.each(msg, function (key, val) {
                                if (episode == 'standby') {
                                    // val[0]: Standby ID
                                    // val[1]: Event
                                    // val[2]: Location
                                    // val[3]: Notes
                                    // val[4]: Start Date
                                    // val[5]: End dDate
                                    $('#standbys').append('<a href="/standby/' + val[0] + '">' + val[1] + ' (' + val[4] + ')</a>');
                                    $('#standbys').append('<br />');
                                }
                            });
                        } else if (episode == 'event') {
                            $('#events').empty();
                            $('#events').append('<br />');
                            $.each(msg, function (key, val) {
                                // val[0]: Event ID
                                // val[1]: Event
                                // val[2]: Location
                                // val[3]: Notes
                                // val[4]: Privileges
                                // val[5]: Start Date
                                // val[6]: End Date
                                $('#events').append('<a href="/event/' + val[0] + '">' + val[1] + ' (' + val[5] + ')</a>');
                                $('#events').append('<br />');
                            });
                        }
                    });
                }
            });

            // Highlights the days in the `dates' array
            function highlightDays(date) {
                for (var i = 0; i < dates.length; i++) {
                    if (new Date(dates[i]).toString() == date.toString())
                        return [true, 'highlight'];
                }

                return [true, ''];
            }
        });
    }

    // Get the Episode days from the server and highlight them on the
    // calendar.
    get_updates();

});
