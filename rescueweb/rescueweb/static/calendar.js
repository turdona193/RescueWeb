// `episode' is a global variable that is defined in every .pt file that uses the
// calendar. `episode' currently only takes on the values `standby' and `event'
// as the only views that currently use this calendar code are the Standby and
// Events calendar.
$(function() {
    var dates = [];
    // CSS rules to color dates. Rules are defined in `tinydropdown.css'.
    var colors = {'standby': 'hilight-purple', 'event': 'hilight-green', 'duty_crew': 'hilight-blue'};

    // Compute the current date
    var currentDate = new Date()
    var day = currentDate.getDate()
    var month = currentDate.getMonth() + 1
    var year = currentDate.getFullYear()

    // Add the *current* month's episodes to the dates array so they can be
    // hilighted.
    addHilightDays(day + "/" + month + "/" + year);

    // Datepicker configs
    $('#datepicker').datepicker({
        // Hilight the days which Episodes occur on
        inline: true,
        changeYear: true,
        yearRange: (year-3) + ':' + (year+3),

        onChangeMonthYear: function(year, month, inst) {
            // Add the days of the month episodes occur on of the month the
            // datepicker is on.
            addHilightDays(1 + "/" + month + "/" + year);
        },

        beforeShowDay: hilightDays,

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
                    // this day and pass along the crew number that's on that
                    // day.
                    //
                    // msg[0]: True if the logged in user is on call for this duty crew
                    // msg[1]: The duty crew number that is on tonight
                    window.location.href = '/duty_crew/' + date.replace(/\//g, '-') + '-' + msg[1];
                }
            });
        }
    });

    // Hilights the days in the `dates' array
    function hilightDays(date) {
        for (var i = 0; i < dates.length; i++) {
            if (new Date(dates[i]).toString() == date.toString())
                return [true, colors[episode]];
        }

        return [true, ''];
    }

    function addHilightDays(date) {
        // Clear out the dates array so we hilight dates for the current month
        dates.length = 0;

        // Add the current month's days to the dates array
        $.ajax({
            url: '/dates.json',
            type: 'GET',
            data: {type: episode, date: date},
            async: false,
            success: function(data) {
                // Add the dates to the dates array so we know which to hilight
                $.each(data, function (key, val) {
                    dates.push(val);
                });
            }
        });
    }

});
