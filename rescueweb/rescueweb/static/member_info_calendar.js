$(function() {
    var episodeTypes = ['standby', 'event', 'duty_crew'];

    // These will hold all of the dates to be colored in by the Datepicker
    var standbyDates = [];
    var eventDates = [];
    var dutyCrewDates = [];

    var episodeDates = {'standby': standbyDates, 'event': eventDates,
                        'duty_crew': dutyCrewDates};

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
        yearRange: '2010:2013',

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
            // Clear out the list
            $('#episodes').empty();

            // Make an AJAX call for every type of episode
            for (var i = 0; i < episodeTypes.length; i++) {
                $.ajax({
                    type: 'GET',
                    url: '/detailed_info.json',
                    data: {date: date, type: episodeTypes[i]},
                    async: false,
                    success: function(msg) {
                        if (episodeTypes[i] == 'standby') {
                            $.each(msg, function (key, val) {
                                // val[0]: Standby ID
                                // val[1]: Event
                                // val[2]: Location
                                // val[3]: Notes
                                // val[4]: Start Date
                                // val[5]: End dDate
                                $('#episodes').append('<li><a href="/standby/' + val[0] + '">' + val[1] + ' (' + val[4] + ')</a></li>');
                            });
                        } else if (episodeTypes[i] == 'event') {
                            $.each(msg, function (key, val) {
                                // val[0]: Event ID
                                // val[1]: Event
                                // val[2]: Location
                                // val[3]: Notes
                                // val[4]: Privileges
                                // val[5]: Start Date
                                // val[6]: End Date
                                $('#episodes').append('<li><a href="/event/' + val[0] + '">' + val[1] + ' (' + val[5] + ')</a></li>');
                            });
                        } else if (episodeTypes[i] == 'duty_crew') {
                            // Redirect the user to the page which contains
                            // information about the duty crew that's on for
                            // this day. Pass along the date in a sanitized way.
                            $('#episodes').append('<li><a href="/duty_crew/' + date.replace(/\//g, '-') + '">This night\'s Duty Crew</a></li>');
                        }
                    }
                });
            }
        }
    });

    // Hilights the days in the `dates' array
    function hilightDays(date) {
        for (var i = 0; i < standbyDates.length; i++) {
            if (new Date(standbyDates[i]).toString() == date.toString())
                return [true, 'hilight-red'];
        }

        for (var i = 0; i < eventDates.length; i++) {
            if (new Date(eventDates[i]).toString() == date.toString())
                return [true, 'hilight-yellow'];
        }

        for (var i = 0; i < dutyCrewDates.length; i++) {
            if (new Date(dutyCrewDates[i]).toString() == date.toString())
                return [true, 'hilight-blue'];
        }

        return [true, ''];
    }

    function addHilightDays(date) {
        // Clear out the dates array so we hilight dates for the current month
        standbyDates.length = 0;
        eventDates.length = 0;
        dutyCrewDates.length = 0;

        for (var i = 0; i < episodeTypes.length; i++) {
            // Add the current month's days to the dates array
            $.ajax({
                url: '/dates.json',
                type: 'GET',
                data: {type: episodeTypes[i], date: date},
                async: false,
                success: function(data) {
                    // Add the dates to the dates array so we know which to hilight
                    $.each(data, function (key, val) {
                        episodeDates[episodeTypes[i]].push(val);
                    });
                }
            });
        }
    }

});
