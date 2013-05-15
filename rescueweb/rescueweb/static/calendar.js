// `episode' is a global variable that is defined in every .pt file that uses the
// calendar. `episode' currently only takes on the values `standby' and `event'
// as the only views that currently use this calendar code are the Standby and
// Events calendar.
$(function() {
    var dates = [];

    // Compute the current date
    var currentDate = new Date()
    var day = currentDate.getDate()
    var month = currentDate.getMonth() + 1
    var year = currentDate.getFullYear()

    // Add the days of the *current* month to be hilighted
    addHilightDays(day + "/" + month + "/" + year, false);

    // Display the calendar
    $('#datepicker').datepicker({
        // Hilight the days which Episodes occur on
        inline: true,
        changeYear: true,
        yearRange: '2010:2013',

        onChangeMonthYear: function(year, month, inst) {
            // Add the days of the *current* month to be hilighted
            addHilightDays(1 + "/" + month + "/" + year, false);
        },

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
                        // val[0]: Standby ID
                        // val[1]: Event
                        // val[2]: Location
                        // val[3]: Notes
                        // val[4]: Start Date
                        // val[5]: End dDate
                        $('#standbys').append('<li><a href="/standby/' + val[0] + '">' + val[1] + ' (' + val[4] + ')</a></li>');
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
                        $('#events').append('<li><a href="/event/' + val[0] + '">' + val[1] + ' (' + val[5] + ')</a></li>');
                    });
                } else if (episode == 'duty_crew') {
                    // Redirect the user to the page which contains
                    // information about the duty crew that's on for
                    // this day. Pass along the date in a sanitized way.
                    window.location.href = '/duty_crew/' + date.replace(/\//g, '-');
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

    function addHilightDays(date, asynchronous) {
        // Clear out the dates array so we hilight dates for the current month
        dates.length = 0;

        // Add the current month's days to the dates array
        $.ajax({
            url: '/dates.json',
            type: 'GET',
            data: {type: episode, date: date},
            async: asynchronous,
            success: function(data) {
                // Add the dates to the dates array so we know which to hilight
                $.each(data, function (key, val) {
                    dates.push(val);
                });
            }
        });
    }

});
