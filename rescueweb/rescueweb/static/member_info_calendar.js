$(function() {
    var episodeTypes = ['standby', 'event', 'duty_crew', 'cert_expire'];

    // These will hold all of the dates to be colored in by the Datepicker
    var standbyDates = [];
    var eventDates = [];
    var dutyCrewDates = [];
    var certExpireDates = [];

    var episodeDates = {'standby': standbyDates, 'event': eventDates,
                        'duty_crew': dutyCrewDates, 'cert_expire': certExpireDates};

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
            // Clear out the list
            $('#episodes').empty();

            // Make an AJAX call for every type of episode
            for (var i = 0; i < episodeTypes.length; i++) {
                $.ajax({
                    type: 'GET',
                    url: '/detailed_info.json',
                    data: {date: date, type: episodeTypes[i], personalized: true},
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
                            // Only add a link to today's duty crew if the user
                            // is signed up for it
                            if (msg == true)
                                $('#episodes').append('<li><a href="/duty_crew/' + date.replace(/\//g, '-') + '">Today\'s Duty Crew</a></li>');
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
                return [true, 'hilight-purple', 'Standby!'];
        }

        for (var i = 0; i < eventDates.length; i++) {
            if (new Date(eventDates[i]).toString() == date.toString())
                return [true, 'hilight-green', 'Event!'];
        }

        for (var i = 0; i < dutyCrewDates.length; i++) {
            if (new Date(dutyCrewDates[i]).toString() == date.toString())
                return [true, 'hilight-blue', 'On Call!'];
        }

        for (var i = 0; i < certExpireDates.length; i++) {
            if (new Date(certExpireDates[i]).toString() == date.toString())
                return [true, 'hilight-red', 'Certificate Expiring!'];
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
                data: {type: episodeTypes[i], date: date, personalized: true},
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
