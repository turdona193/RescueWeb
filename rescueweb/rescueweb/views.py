import calendar
import datetime
import random
import os
import re

from pyramid.response import Response
from pyramid.view import view_config
from pyramid.renderers import get_renderer

from sqlalchemy.exc import DBAPIError
from sqlalchemy.exc import IntegrityError
from sqlalchemy import distinct
from sqlalchemy import func

#from pyramid_mailer import get_mailer
#from pyramid_mailer.message import Message


from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound,
    )

from pyramid.view import (
    view_config,
    forbidden_view_config,
    )

from pyramid.security import (
    remember,
    forget,
    authenticated_userid,
    )


from .models import (
    DBSession,
    Page,
    Announcements,
    Documents,
    Events,
    Users,
    Certifications,
    Privileges,
    OperationalStatus,
    AdministrativeStatus,
    EboardPositions,
    TrainingLevel,
    WebLinks,
    StandBy,
    MeetingMinutes,
	Pictures,
    StandByPersonnel,
    Attendees,
    DutyCrews,
    DutyCrewCalendar,
    DutyCrewSchedule,
    LoginIns,
    EboardPositions
    )

TABLE_DICT = {'standby' : StandBy, 'event' : Events}

@view_config(route_name='home', renderer='templates/home.pt')
def home(request):
    main = get_renderer('templates/template.pt').implementation()
    page = DBSession.query(Page).filter_by(name='Home').first()

    return dict(
            title='Home', 
            main=main, 
            page=page,
            user=request.user
            )

@view_config(route_name='history', renderer='templates/history.pt')
def history(request):
    main = get_renderer('templates/template.pt').implementation()
    page = DBSession.query(Page).filter_by(name='History').first()

    return dict(
            title='History', 
            main=main, 
            page=page,
            user=request.user
            )

@view_config(route_name='personnel', renderer='templates/personnel.pt')
def personnel(request):
    main = get_renderer('templates/template.pt').implementation()
    page = DBSession.query(Users.portablenumber, Users.fullname,
			AdministrativeStatus.status, OperationalStatus.status).\
			join(AdministrativeStatus) .join(OperationalStatus).order_by(Users.portablenumber)
    headers = ['Portable', 'Name', 'Administrative', 'Operational']

    return dict(
            title='Personnel', 
            main=main, 
            personnel=page, 
            headers=headers,
            user=request.user
            )


@view_config(route_name='announcements', renderer='templates/announcements.pt')
def announcements(request):
    main = get_renderer('templates/template.pt').implementation()
    announcements = DBSession.query(Announcements).order_by(Announcements.posted.desc()).all()
    headers = [column.name for column in announcements[0].__table__.columns]

    return dict(
            title='Announcements', 
            main=main,
            announcements=announcements,
            headers=headers,
            user=request.user)
    
@view_config(route_name='events', renderer='templates/events.pt')
def event_table(request):
    main = get_renderer('templates/template.pt').implementation()
    event_list = DBSession.query(Events).all()

    return dict(
            title='Events', 
            main=main,
            user=request.user
            )

@view_config(route_name='event', renderer='templates/event.pt')
def event(request):
    """Renders information relating to a specific Event"""
    main = get_renderer('templates/template.pt').implementation()

    # Sanity check
    if 'eventid' not in request.matchdict:
        return HTTPNotFound('No event passed in.')

    # Get the user's information if they are signed up for an event
    attendee = DBSession.query(Attendees).\
            filter(Attendees.eventid == request.matchdict['eventid']).\
            filter(Attendees.username == get_username(request)).first()

    # Check to see if we got here by signing up for the standby
    if 'signup.submitted' in request.params and not attendee:
        attendee = Attendees(
                eventid=request.matchdict['eventid'],
                username=get_username(request)
                )
        DBSession.add(attendee)
    elif 'retract_attendance.submitted' in request.params and attendee:
        DBSession.delete(attendee)
        attendee = None

    # Get the event that was chosen and the headers to display it
    event = DBSession.query(Events.name, Events.location, Events.notes,
            Events.privileges, Events.startdatetime, Events.enddatetime).\
            filter(Events.eventid == request.matchdict['eventid']).\
            first()

    event_headers = ['Event', 'Location', 'Notes', 'Privileges',
            'Start Date Time', 'End Date Time']

    # Get the personnel that are signed up for the event and the headers that
    # are used to display the information.
    attendees = DBSession.query(
            Attendees.eventid,
            Attendees.username).\
            filter(Attendees.eventid == request.matchdict['eventid']).all()

    attendees_headers = ['Event ID', 'User']

    return dict(
            title=event.name,
            event=zip(event_headers, event),
            attendees=attendees,
            attendees_headers=attendees_headers,
            user_already_registered=attendee,
            main=main,
            user=request.user
            )

@view_config(route_name='join', renderer='templates/join.pt')
def join(request):
    main = get_renderer('templates/template.pt').implementation()
    page = DBSession.query(Page).filter_by(name='Join').first()

    return dict(
            title='How to Join',
            main=main,
            page=page,
            user=request.user
            )
    
@view_config(route_name='contact', renderer='templates/contact.pt')
def contact(request):
    main = get_renderer('templates/template.pt').implementation()
    page = DBSession.query(Page).filter_by(name='ContactUs').first()

    return dict(
            title='Contact Us', 
            main=main,
            page=page,
            user=request.user
            )
    
@view_config(route_name='links', renderer='templates/links.pt')
def links(request):
    main = get_renderer('templates/template.pt').implementation()
    page = DBSession.query(WebLinks).all()
    headers = [column.name for column in page[0].__table__.columns]

    return dict(
            title='Links', 
            main=main,
            links=page, 
            header=headers,
            user=request.user
            )

@view_config(route_name='documents', renderer='templates/documents.pt',
             permission='Member')
def documents(request):
    main = get_renderer('templates/template.pt').implementation()
    page = DBSession.query(Documents).all()
    headers = [column.name for column in page[0].__table__.columns]

    return dict(
            title='Squad Documents', 
            main=main,
            page=page, 
            header=headers,
            user=request.user
            )

@view_config(route_name='minutes', renderer='templates/minutes.pt',
             permission='Member')
def minutes(request):
    main = get_renderer('templates/template.pt').implementation()
    #init empty fields
    meeting_minutes = []
    selected=False
    
    all_dates = DBSession.query(MeetingMinutes.datetime).group_by(MeetingMinutes.datetime).order_by(MeetingMinutes.datetime.desc()).all()
    all_dates_list = [minute.datetime.timetuple()[:3] for minute in all_dates]

    if "date.selected" in request.params:
        selected=True

        selected_date = request.params['selected_date']
        date = datetime.datetime.strptime(selected_date,'(%Y, %m, %d)')
        meeting_minutes = DBSession.query(MeetingMinutes).\
        filter_by(datetime = date).\
        order_by(MeetingMinutes.datetime.desc()).all()
    
    return dict(
            title='Meeting Minutes',
            main=main,
            selected = selected,
            meeting_minutes=meeting_minutes,
            all_dates=all_dates_list,
            user=request.user
            )

@view_config(route_name='member_info', renderer='templates/member_info.pt',
             permission='Member')
def member_info(request):
    main = get_renderer('templates/template.pt').implementation()
    user = request.user
    message = ''
    certs = ''
    hascert = DBSession.query(Certifications).filter(Certifications.username == user.username).count()
    if hascert:
        all_certs = DBSession.query(Certifications).filter(Certifications.username == user.username).all()
        certs = [[cert.certification,cert.certnumber,cert.expiration] for cert in all_certs]
    return dict(
            title='Member Information',
            main=main,
            user=user,
            message=message,
            hascert=hascert,
            certs=certs
            )
    
@view_config(route_name='standbys', renderer='templates/standbys.pt',
             permission='Member')
def standbys(request):
    """A view that diplays a javascript calendar with dates with Standbys
    hilighted.

    This view is very simple because all the work happens after the page gets
    loaded with javascript.

    """
    main = get_renderer('templates/template.pt').implementation()

    return dict(
            title='Stand-Bys', 
            main=main,
            user=request.user
            )

@view_config(route_name='standby', renderer='templates/standby.pt',
             permission='Member')
def standby(request):
    """Renders information relating to a specific Standby event"""
    main = get_renderer('templates/template.pt').implementation()

    # Sanity check
    if 'standbyid' not in request.matchdict:
        return HTTPNotFound('No standby passed in.')

    # Get the user's information if they are signed up for the standby
    standby_person = DBSession.query(StandByPersonnel).\
            filter(StandByPersonnel.standbyid == request.matchdict['standbyid']).\
            filter(StandByPersonnel.username == get_username(request)).first()

    # Check to see if we got here by signing up for the standby
    if 'signup.submitted' in request.params:
        if 'position' not in request.POST:
            return Response('Error: You have to sign up with either Active or '
            'Probationary status')

        # Only add the user to the Standby table if they weren't already signed
        # up. If they are already signed up, just bring them back to the page.
        if standby_person:
            return HTTPFound(location=request.url)
        else:
            standby_person = StandByPersonnel(
                    standbyid=request.matchdict['standbyid'],
                    username=get_username(request),
                    standbyposition=request.POST['position'],
                    coverrequested=False
                    )
            DBSession.add(standby_person)
    elif 'coverage_request.submitted' in request.params:
        standby_person.coverrequested = True
    elif 'cancel_coverage_request.submitted' in request.params:
        standby_person.coverrequested = False

    # Get the standby event that was chosen and the headers to display it
    standby = DBSession.query(StandBy.event, StandBy.location, StandBy.notes,
            StandBy.startdatetime, StandBy.enddatetime).\
            filter(StandBy.standbyid == request.matchdict['standbyid']).\
            first()

    standby_headers = [
            'Event', 
            'Location', 
            'Notes', 
            'Start Date Time', 
            'End Date Time'
            ]

    # Get the personnel that are signed up for the standby and the headers that
    # are used to display the information.
    standby_personnel = DBSession.query(
            StandByPersonnel.standbyid,
            StandByPersonnel.username,
            StandByPersonnel.standbyposition,
            StandByPersonnel.coverrequested).\
                    filter(StandByPersonnel.standbyid ==
                    request.matchdict['standbyid']).all()

    standby_personnel_headers = [
            'Standby ID',
            'User', 
            'Standby Position', 
            'Requesting Coverage'
            ]

    # Flag the user as requesting coverage or not
    if standby_person:
        # Don't refactor this test. It really and truly has to be the way it is!
        requesting_coverage = standby_person.coverrequested
    else:
        requesting_coverage = False

    return dict(
            title=standby.event,
            standby=zip(standby_headers, standby),
            standby_personnel=standby_personnel,
            standby_personnel_headers=standby_personnel_headers,
            user_already_registered=standby_person,
            requesting_coverage=requesting_coverage,
            main=main,
            user=request.user
            )

@view_config(name='dates.json', renderer='json')
def dates(request):
    """Serves up Event and StandBy dates via JSON back to the calendar. 
    
    This function is called when the calendar is first loaded. The calendar uses
    this information to highlight days Events or Standbys are going on.

    """
    # Ensure the requester specified whether they want StandBy or Events dates
    if 'type' not in request.GET:
        return None

    episode_query = DBSession.query(TABLE_DICT[request.GET['type']])
    # If querying events, cut down the events to only those that the user has
    # the appropriate privilege levels to see.
    if request.GET['type'] == 'event':
        episode_query = episode_query.filter(
                Events.privileges <= get_privilege_value(request))
    episode_query = episode_query.all()

    return [ 
        (
            '{}/{}/{}'.format(
                episode.startdatetime.month, 
                episode.startdatetime.day,
                episode.startdatetime.year
                             ),
            '{}/{}/{}'.format(
                episode.enddatetime.month,
                episode.enddatetime.day, 
                episode.enddatetime.year
                             )
        ) for episode in episode_query 
           ]

@view_config(name='detailed_info.json', renderer='json')
def detailed_info(request):
    """Serves up information about Standbys on a particular date via JSON"""
    if 'date' not in request.GET or 'type' not in request.GET:
        # No date was sent or the type of information was not specified
        return None

    # Grab the date and type of information desired from the AJAX request
    month, day, year = request.GET['date'].split('/')
    episode_date = datetime.datetime(int(year), int(month), int(day))
    Table = TABLE_DICT[request.GET['type']]
    episode_query = DBSession.query(Table)\
            .filter(Table.startdatetime == episode_date)

    # Return all of the StandBy dates occurring on this date
    if request.GET['type'] == 'standby':
        return [
            (
                episode.standbyid,
                episode.event,
                episode.location,
                episode.notes,
                str(episode.startdatetime),
                str(episode.enddatetime),
            ) for episode in episode_query 
               ]
    # Return all of the StandBy dates occurring on this date
    else:
        assert request.GET['type'] == 'event'
        episode_query = episode_query.filter(Events.privileges <=
                get_privilege_value(request))

        return [
            (
                episode.eventid,
                episode.name,
                episode.location,
                episode.notes,
                episode.privileges,
                str(episode.startdatetime),
                str(episode.enddatetime),
            ) for episode in episode_query
               ]

@view_config(route_name='duty_crew_calendar',
             renderer='templates/duty_crew_calendar.pt', permission='Member')
def duty_crew_calendar(request):
    main = get_renderer('templates/template.pt').implementation()
    year = 0
    month = 0
    if 'form.changedate' in request.params:
        if request.params['form.changedate'] == '<--':
            year = int(request.params['yearNum'])
            month = int(request.params['monthNum']) - 1
            if month < 1:
                month = 12
                year = year - 1
        if request.params['form.changedate'] == '-->':
            year = int(request.params['yearNum'])
            month = int(request.params['monthNum']) + 1
            if month > 12:
                month = 1
                year = year + 1
    else:
        currentDate = datetime.date.today()
        year = currentDate.year
        month = currentDate.month
    monthName = calendar.month_name[month]
    startDay, days = calendar.monthrange(year, month)
    startDay = (startDay +1)%7

    return dict(
            title='Duty Crew Calendar',
            monthName=monthName,
            startDay=startDay,
            yearNum=year,
            monthNum=month,
            days=days,
            main=main,
            user=request.user
            )

@view_config(route_name='coverage', renderer='templates/coverage.pt',
             permission='Member')
def coverage(request):
    main = get_renderer('templates/template.pt').implementation()
    standby_requests = DBSession.query(StandByPersonnel.username,
                                       StandByPersonnel.standbyid,
                                       StandByPersonnel.standbyposition,
                                       StandBy.event,
                                       StandBy.startdatetime,
                                       ).join(StandBy).filter(StandByPersonnel.coverrequested == True).all()
    all_standby_requests = [[standby.standbyid, standby.event, standby.startdatetime, standby.username, standby.standbyposition] for standby in standby_requests]
    duty_crew_requests = DBSession.query(DutyCrewSchedule).filter_by(coveragerequest = True).all()
    all_duty_crew_requests = [[crew.day, crew.username] for crew in duty_crew_requests]
    return dict(
            title='Coverage Requests',
            main=main,
            standby_requests=all_standby_requests,
            duty_crew_requests=all_duty_crew_requests,
            user=request.user
            )
    
@view_config(route_name='add_user', renderer='templates/add_user.pt',
             permission='admin')
def add_user(request):
    main = get_renderer('templates/template.pt').implementation()
    message = ''
    monthlist = [['January', 1],[ 'February', 2],[ 'March', 3],[ 'April',4],[ 'May', 5],[ 'June', 6],
                 ['July', 7],[ 'August', 8],[ 'September', 9],[ 'October', 10],[ 'November', 11],[ 'December', 12]]

    if 'form.submitted' in request.params:
        new_username_string = request.params['username']
        new_user_exists = DBSession.query(Users).filter_by(username = new_username_string).first()
        if new_user_exists:
            message = 'That username exist, Please select a new one'
        else:
            DBSession.add(Users(
                username = request.params['username'],
                password = request.params['password'],
                firstname = request.params['firstname'],
                middlename = request.params['middlename'],
                lastname = request.params['lastname'],
                birthday = datetime.date(int(request.params['year']),int(request.params['month']),int(request.params['day'])),
                street = request.params['street'],
                city = request.params['city'],
                state = request.params['state'],
                zipcode = request.params['zipcode'],
                residence = request.params['residence'],
                roomnumber = request.params['roomnumber'],
                phonenumber = request.params['phonenumber'],
                email = request.params['email'],
                privileges = request.params['privileges'],
                trainingvalue = request.params['trainingvalue'],
                administrativevalue = request.params['administrativevalue'],
                operationalvalue = request.params['operationalvalue'],
                portablenumber = 0
                ))
            
    Options = DBSession.query(Privileges).all()
    privilegesOptions = [[option.privilegevalue ,option.privilege] for option in Options]
    Options = DBSession.query(TrainingLevel).all()
    trainingOptions = [[option.trainingvalue, option.traininglevel] for option in Options]
    Options = DBSession.query(AdministrativeStatus).all()
    administrativeOptions = [[option.administrativevalue, option.status] for option in Options]
    Options = DBSession.query(OperationalStatus).all()
    operationalOptions = [[option.operationalvalue,option.status] for option in Options]
    
    return dict(
            title='Add User',
            main=main,
            monthlist = monthlist,
            message=message,
            privilegesOptions=privilegesOptions,
            trainingOptions=trainingOptions,
            administrativeOptions=administrativeOptions,
            operationalOptions=operationalOptions,
            user=request.user
            )

@view_config(route_name='edit_user', renderer='templates/edit_user.pt',
             permission='admin')
def edit_user(request):
    main = get_renderer('templates/template.pt').implementation()
    message = ''
    userselected = ''
    monthlist = [['January', 1],[ 'February', 2],[ 'March', 3],[ 'April',4],[ 'May', 5],[ 'June', 6],
                 ['July', 7],[ 'August', 8],[ 'September', 9],[ 'October', 10],[ 'November', 11],[ 'December', 12]]
    
    if 'userselected' in request.params:
        userselected = request.params['userselected']
    
    if 'form.submitted' in request.params:
        edit_username_string = request.params['username']
        userselected = request.params['userselected']
        edit_username_exists = DBSession.query(Users).filter_by(username = edit_username_string).first()
        if edit_username_exists and not edit_username_exists.username == userselected :
            message = 'That username exist, Please select a new one'
        else:
            userselected = request.params['userselected']
            edited_user = DBSession.query(Users).filter_by(username=userselected).first()
            edited_user.username = edit_username_string
            edited_user.password = request.params['password']
            edited_user.firstname = request.params['firstname']
            edited_user.middlename = request.params['middlename']
            edited_user.lastname = request.params['lastname']
            edited_user.birthday = datetime.date(int(request.params['year']), int(request.params['month']), int(request.params['day']))
            edited_user.street = request.params['street']
            edited_user.city = request.params['city']
            edited_user.state = request.params['state']
            edited_user.zipcode = request.params['zipcode']
            edited_user.residence = request.params['residence']
            edited_user.roomnumber = request.params['roomnumber']
            edited_user.phonenumber = request.params['phonenumber']
            edited_user.email = request.params['email']
            edited_user.privileges = request.params['privileges']
            edited_user.trainingvalue = request.params['trainingvalue']
            edited_user.administrativevalue = request.params['administrativevalue']
            edited_user.operationalvalue = request.params['operationalvalue']
            DBSession.add(edited_user)
        
    if 'form.selected' in request.params:
        userselected = request.params['selecteduser']
        edited_user = DBSession.query(Users).filter_by(username=userselected).first()
    else:
        userselected = ''
        edited_user = Users('','','','','','','','','','','','','','','','','','','')

    Options = DBSession.query(Privileges).all()
    privilegesOptions = [[option.privilegevalue ,option.privilege] for option in Options]
    Options = DBSession.query(TrainingLevel).all()
    trainingOptions = [[option.trainingvalue, option.traininglevel] for option in Options]
    Options = DBSession.query(AdministrativeStatus).all()
    administrativeOptions = [[option.administrativevalue, option.status] for option in Options]
    Options = DBSession.query(OperationalStatus).all()
    operationalOptions = [[option.operationalvalue,option.status] for option in Options]
    
    allusers = DBSession.query(Users).order_by(Users.username).all() 
    allusernames = [auser.username for auser in allusers]
    
    return dict(
            title='Edit User',
            main=main,
            message=message,
            userselected=userselected,
            edited_user=edited_user,
            users=allusernames,
            monthlist=monthlist,
            privilegesOptions=privilegesOptions,
            trainingOptions=trainingOptions,
            administrativeOptions=administrativeOptions,
            operationalOptions=operationalOptions,
            user=request.user,
            )

@view_config(route_name='delete_user', renderer='templates/delete_user.pt',
             permission='admin')
def delete_user(request):
    main = get_renderer('templates/template.pt').implementation()
    message = ''
    
    if 'form.submitted' in request.params:
        user_selected = request.params['delete_user']
        deleted_user = DBSession.query(Users).filter_by(username=user_selected).first()
        if deleted_user:
            name = deleted_user.username
            DBSession.delete(deleted_user)
            message = "{} has been deleted".format(name)
        else:
            message = "Please select a vaild username"

    allusers = DBSession.query(Users).order_by(Users.username).all() 
    allusernames = ["None"]+[auser.username for auser in allusers]

    return dict(
            title='Delete User', 
            main=main,
            allusernames=allusernames,
            message=message,
            user=request.user
            )

@view_config(route_name='edit_pages', renderer='templates/edit_pages.pt',
             permission='admin')
def edit_pages(request):
    main = get_renderer('templates/template.pt').implementation()
    pagenames = ['Home', 'History', 'Join', 'ContactUs'] 
    if 'form.submitted' in request.params:
        pageselected = request.params['editpage']
        page = DBSession.query(Page).filter_by(name = pageselected).first()
        page.data = request.params['body']
        DBSession.add(page)
        #return HTTPFound(location = request.route_url('home'))

    if 'form.selected' in request.params:
        pageselected = request.params['pagename']
        page = DBSession.query(Page).filter_by(name=pageselected).first()
        content = 'this should be after the load'
    else:
        page = Page('' ,'')
        pageselected = ''
        
    return dict(
            title = 'Edit Pages', 
            main = main, 
            page = page, 
            pagenames = pagenames, 
            pageselected = pageselected,
            user=request.user
            )

@view_config(route_name='add_edit_links', renderer='templates/add_edit_links.pt',
             permission='admin')
def add_edit_links(request):
    main = get_renderer('templates/template.pt').implementation()
    linkchosen = ''
    selected = ''
    message = 'Please select to Create a New Link or Edit/Delete an Existing one'
    link = WebLinks("","")
    if 'form.selected' in request.params:
        selected = request.params['form.selected']
        linkname = request.params['selectlink']
        if selected == 'New' or linkname == 'New':
            link = WebLinks("New","")
            message = 'You have selected to Create a new link'
        if selected == 'Load' and not linkname == 'New':
            link = DBSession.query(WebLinks).filter_by(name=request.params['selectlink']).first()
            linkchosen = link.name
            message = 'You have selected to Edit an existing link'
        if selected =='Delete':
            if linkname == "New":
                message = "Please Select a valid Link to delete/load or create a new link"
            else:
                link = DBSession.query(WebLinks).filter_by(name=request.params['selectlink']).first()
                DBSession.delete(link)
                message = 'You have selected to Delete {}'.format(link.name)

    if 'form.submitted' in request.params:
        name_of = request.params['name']
        address_of=request.params['address']
        if name_of and address_of:
            link = DBSession.query(WebLinks).filter_by(name=name_of).first()
            if link:
                link.name=name_of
                link.address=address_of
            else:
                link = WebLinks(name=name_of, address=address_of)
            
            DBSession.add(link)
            message="{} has been entered something".format(name_of)
        else:
            message="Please enter something in both fields"
            selected = request.params['selected']


    links = DBSession.query(WebLinks).all()
    linknames = ['New']+[weblink.name for weblink in links]

    return dict(
            title='Add/Edit Links', 
            main=main,
            link=link,               #link to be edited and added to the database
            linknames=linknames,     #name of all the links
            selected = selected,     #If you chosen new,load,delete
            message=message,         #Message to the User
            user=request.user
            )

@view_config(route_name='add_edit_documents', renderer='templates/add_edit_documents.pt',
             permission='admin')
def add_edit_documents(request):
    main = get_renderer('templates/template.pt').implementation()
    form = ''
    if 'form.operation' in request.params:
        operation = request.params['form.operation']
        if operation == 'Add New':
            form='New'
        if operation =='Delete':
            form='Delete'
            doc = eval(request.params['document_selected'])
            document = DBSession.query(Documents).filter(Documents.name==doc[0]).filter(Documents.filename==doc[1]).first()
            DBSession.delete(document)
        
    if 'form.submitted' in request.params:
        form=''
        filename = request.POST['doc'].filename
        input_file = request.POST['doc'].file
        file_path = os.path.join('rescueweb/documents', '{}'.format(filename))
        temp_file_path = file_path + '~'
        output_file = open(temp_file_path, 'wb')
        input_file.seek(0)
        while True:
            data = input_file.read(2<<16)
            if not data:
                break
            output_file.write(data)
        output_file.flush()
        output_file.close()
        os.rename(temp_file_path, file_path)
        
        name = request.params['doc_name']
        DBSession.add(
                      Documents(
                                name=name,
                                filename=filename,
                                )
                      )
        
    all_documents = DBSession.query(Documents).all()
    all_documents_list = [[adoc.name,adoc.filename] for adoc in all_documents]
    

    return dict(
            title='Add/Edit Documents',
            main=main,
            form=form,
            all_documents_list=all_documents_list,
            user=request.user
            
            )

@view_config(route_name='add_edit_minutes', renderer='templates/add_edit_minutes.pt',
             permission='admin')
def editmeetingminutes(request):
    main = get_renderer('templates/template.pt').implementation()
    #collect all Meeting Minutes
    allminutes = DBSession.query(MeetingMinutes.datetime).group_by(MeetingMinutes.datetime).order_by(MeetingMinutes.datetime.desc()).all()
    alldates = [minute.datetime.timetuple()[:3] for minute in allminutes]
    #Initialize Empty fields
    date_selected = False
    minute_selected = False
    allminutes = []
    selected_date = 'New'
    selected_minute = MeetingMinutes('','','','')
    message = ''
    date = ''
    form = ''
    
    if 'form.new' in request.params:
        date_selected = True
        minute_selected = True
        form = 'New'
    
    if 'date.selected' in request.params:
        operation = request.params['date.selected']
        selected_date = request.params['selected_date']
        date = datetime.datetime.strptime(selected_date,'(%Y, %m, %d)')
        allminutesdatabase = DBSession.query(MeetingMinutes.header,MeetingMinutes.subheader).filter_by(datetime = date).all()
        if operation == 'Load':
            form='Load'
            date_selected = True
            message = 'Loaded {}'.format(date.timetuple()[:3])
            allminutes = [['New','New']]+[[minutes.header,minutes.subheader] for minutes in allminutesdatabase]
        if operation == 'Delete':
            form='Delete'
            message = 'Deleted {}'.format(date.timetuple()[:3])
            DBSession.delete(allminutesdatabase)
            
    if 'report.selected' in request.params:
        operation = request.params['report.selected']
        if operation == 'New':
            form = 'New'
        else:
            selected_date = request.params['use_date']
            string_of_list = request.params['selected_report']
            list = eval(string_of_list)
            minute = DBSession.query(MeetingMinutes).\
            filter(MeetingMinutes.datetime == datetime.datetime.strptime(selected_date,'(%Y, %m, %d)')).\
            filter(MeetingMinutes.header == list[0]).\
            filter(MeetingMinutes.subheader == list[1]).\
            first()
            if not minute:
                form='New'
                minute = MeetingMinutes('','','','')
                message = "Message did not exist... Don't know why"
            if operation == 'Load':
                date_selected = True
                minute_selected = True
                selected_minute = minute
                form='Load'
            if operation == 'Delete':
                form='Delete'
                date_selected = False
                minute_selected = False
                message = 'Deleted {}'.format(date.timetuple()[:3])
                DBSession.delete(minute)
                
    if 'form.submitted' in request.params:
        operation = request.params['form']
        date_string = request.params['date_time']
        date_object = datetime.datetime.strptime(date_string,'%Y-%m-%d')
        if operation == 'New':
            DBSession.add(
                MeetingMinutes(
                    datetime = date_object,
                    header = request.params['header'],
                    subheader = request.params['subheader'],
                    content = request.params['body'],
                    ))
            message = "Record Edited by new"
        if operation == 'Load':
            selected_minute_string = request.params['use_minute']
            selected_minute_list = eval(selected_minute_string)
            selected_minute = DBSession.query(MeetingMinutes).\
            filter(MeetingMinutes.datetime == date_object).\
            filter(MeetingMinutes.header == selected_minute_list[0]).\
            filter(MeetingMinutes.subheader == selected_minute_list[1]).\
            first()
            if selected_minute:
                selected_minute.datetime = date_object
                selected_minute.header = request.params['header']
                selected_minute.subheader = request.params['subheader']
                selected_minute.content = request.params['body']
                DBSession.add(selected_minute)
                message = "Record Edited by load"

        date_selected = False
        minute_selected = False
            
    return dict(
            title='Add/Edit Meeting Minutes',
            main=main,
            alldates=alldates,
            allminutes=allminutes,
            form=form,
            message=message,
            user=request.user,
            selected_date=selected_date,       #date that is selected
            selected_minute=selected_minute,   #minute that is selected
            date_selected = date_selected,     #boolean
            minute_selected = minute_selected, #boolean
            )

@view_config(route_name='add_edit_pictures', renderer='templates/add_edit_pictures.pt',
             permission='admin')
def add_edit_pictures(request):
    main = get_renderer('templates/template.pt').implementation()

    form = ''
    if 'form.operation' in request.params:
        operation = request.params['form.operation']
        if operation == 'Add_New':
            form='New'
        if operation =='Delete':
            form='Delete'
            pic = eval(request.params['picture_selected'])
            document = DBSession.query(Pictures).filter(Pictures.pictureindex==pic[0]).first()
            DBSession.delete(document)
        
    if 'form.submitted' in request.params:
        form=''
        filename = request.POST['pic'].filename
        input_file = request.POST['pic'].file
        file_path = os.path.join('rescueweb/static/pictures/', '{}'.format(filename))
        #print(file_path)
        #some_path = request.static_url('rescueweb:documents/')
        #print(some_path)
        temp_file_path = file_path + '~'
        output_file = open(temp_file_path, 'wb')
        input_file.seek(0)
        while True:
            data = input_file.read(2<<16)
            if not data:
                break
            output_file.write(data)
        output_file.flush()
        output_file.close()
        os.rename(temp_file_path, file_path)
        
        category = request.params['pic_cate']
        description = request.params['body']
        DBSession.add(
                      Pictures(
                                picture = filename,
                                description = description,
                                category = category
                                )
                      )
        
    all_pictures = DBSession.query(Pictures).order_by(Pictures.category).all()
    all_pictures_list = [[apic.pictureindex,apic.category,apic.picture] for apic in all_pictures]
    
    return dict(
            title='Add/Edit Pictures',
            main=main,            
            form=form,
            all_pictures_list=all_pictures_list,
            user=request.user
            )

@view_config(route_name='edit_portable_numbers', renderer='templates/edit_portable_numbers.pt',
             permission='admin')
def edit_portable_numbers(request):
    main = get_renderer('templates/template.pt').implementation()
    
    if 'form.submitted' in request.params:
        allusers = DBSession.query(Users).order_by(Users.portablenumber).all() 
        for changeuser in allusers:
            i = int(request.params[changeuser.username])
            if i:
                changeuser.portablenumber = i
                DBSession.add(changeuser)        
    allusers = DBSession.query(Users).order_by(Users.portablenumber).all() 
    allusernames = [[auser.fullname ,auser.username, auser.portablenumber] for auser in allusers]
    
    return dict(
            title='Edit Portable Numbers', 
            main=main,
            allusernames=allusernames,
            user=request.user
            )

@view_config(route_name='add_edit_certifications', renderer='templates/add_edit_certifications.pt',
             permission='admin')
def add_edit_certifications(request):
    main = get_renderer('templates/template.pt').implementation()
        # used to list the names so a user can be selected
    all_users = DBSession.query(Users).order_by(Users.username).all()
    all_usernames = [auser.username for auser in all_users]

    result = '' # stores message to be displayed after a change is made to a certification
    selected_user = ''
    selected_cert = ''
    name_of_certs = []
    certifications = DBSession.query(Certifications).all()
    form = ''

        # if a user has been selected
    if 'form.selected' in request.params:
        selected_user = request.params['selectlink']
        certifications = DBSession.query(Certifications).filter_by(username = selected_user).all()
        name_of_certs = [certs.certification for certs in certifications]
        form = 'userLoad'

        # if a certification has been selected
    if 'form.certselected' in request.params:
        selected_user = request.params['suser']
        selected_cert = request.params['selectcert']
        if selected_cert == 'New':
            certifications = Certifications('','','','')
        else:
            certifications = DBSession.query(Certifications).filter_by(username = selected_user)\
                         .filter_by(certification = selected_cert).first()
        form = 'Edit Cert'

        # after a certification has been added/edited/deleted
    if 'form.updated' in request.params:
        if request.params['scert'] == 'New':
            cert = Certifications('','','','')
            cert.username = request.params['suser']
            cert.certification = request.params['certname']
            cert.certnumber = request.params['certnum']
            cert.expiration = request.params['exp']
            DBSession.add(cert)
            result = 'Certification added.'
        elif request.params['form.updated'] == 'Delete':
            user = request.params['suser']
            certname = request.params['scert']
            cert = DBSession.query(Certifications).filter_by(username = user)\
                   .filter_by(certification = certname).first()
            DBSession.delete(cert)
            result = 'Certification deleted.'
        else:
            user = request.params['suser']
            certname = request.params['scert']
            cert = DBSession.query(Certifications).filter_by(username = user)\
                   .filter_by(certification = certname).first()
            cert.certnumber = request.params['certnum']
            cert.expiration = request.params['exp']
            result = 'Certification edited.'
        certifications = DBSession.query(Certifications).filter_by(username = selected_user).all()
        name_of_certs = [certs.certification for certs in certifications]
                         
    return dict(
            title='Add/Edit Certifications',
            main=main,
            all_users = all_usernames,
            form=form,
            certlist=name_of_certs,
            certifications=certifications,
            selected_user=selected_user,
            selected_cert=selected_cert,
            result=result,
            user=request.user
            )
    
@view_config(route_name='add_edit_standby', renderer='templates/add_edit_standby.pt',
             permission='admin')
def add_edit_standby(request):
    main = get_renderer('templates/template.pt').implementation()
    standbychosen = ''
    standby = ''
    form = ''
    dateError = ''

    if 'form.submitted' in request.params:
        if request.params['option'] == 'New':
            standby = StandBy('','','','','')
            standby.standbyid = 1 + DBSession.query(StandBy).count()
            standby.event = request.params['event']
            standby.location = request.params['location']
            standby.notes = request.params['notes']
            try:
                standby.startdatetime = datetime.datetime.strptime(request.params['startdatetime'],'%Y, %m, %d')
                standby.enddatetime = datetime.datetime.strptime(request.params['enddatetime'],'%Y, %m, %d')
                DBSession.add(standby)
            except:
                dateError = 'improper date entry, please use the following format: YYYY, MM, DD'
        if request.params['option'] == 'Load':
            editstandby = request.params['editstandby']
            standby = DBSession.query(StandBy).filter_by(event = editstandby).first()
            standby.event = request.params['event']
            standby.location = request.params['location']
            standby.notes = request.params['notes']
            try:
                standby.startdatetime = datetime.datetime.strptime(request.params['startdatetime'],'%Y, %m, %d')
                standby.enddatetime = datetime.datetime.strptime(request.params['enddatetime'],'%Y, %m, %d')
                DBSession.add(standby)
            except:
                dateError = 'improper date entry, please use the following format: YYYY, MM, DD'
        return HTTPFound(location = request.route_url('standbys'))

    if 'form.selected' in request.params:
        if request.params['form.selected'] == 'New':
            standbychosen = ''
            standby = StandBy('','','','','')
            form = 'New'
        if request.params['form.selected'] == 'Load':
            standbychosen = request.params['selectedstandby']
            standby = DBSession.query(StandBy).filter_by(event=standbychosen).first()
            form = 'Load'
        if request.params['form.selected'] == 'Delete':
            standbychosen = request.params['selectedstandby']
            standby = DBSession.query(StandBy).filter_by(event=standbychosen).first()
            DBSession.delete(standby)
            return HTTPFound(location = request.route_url('standbys'))

    else:
        stanby = StandBy('','','','','')
        standbychosen = ''


    get_all_standBy = DBSession.query(StandBy).all()
    all_standBy = [standB.event for standB in get_all_standBy]
    return dict(title='Add/Edit Standby',
            main=main,
            all_standBy=all_standBy,
	    standby = standby,
	    standbychosen=standbychosen,
	    form=form,
            dateError = dateError,
            user=request.user
            )

@view_config(route_name='edit_duty_crew', renderer='templates/edit_duty_crew.pt',
             permission='admin')
def edit_duty_crew(request):
    main = get_renderer('templates/template.pt').implementation()

    #Stores the number of crews.
    numOfCrews = DBSession.query(func.max(DutyCrews.crewnumber)).scalar()

    year = 0
    month = 0
    if 'form.changedate' in request.params:
        if request.params['form.changedate'] == '<--':
            year = int(request.params['yearNum'])
            month = int(request.params['monthNum']) - 1
            if month < 1:
                month = 12
                year = year - 1
        if request.params['form.changedate'] == '-->':
            year = int(request.params['yearNum'])
            month = int(request.params['monthNum']) + 1
            if month > 12:
                month = 1
                year = year + 1
    elif 'form.submitted' in request.params:
        year = int(request.params['yearNum'])
        month = int(request.params['monthNum'])
        startDay, days = calendar.monthrange(year, month)

            #for i in range(number of days in the month)
        for i in range(days):
            crewNum = request.params['{}'.format(i+1)]
            print("!!!!!{}:{}!!!!".format(i+1,crewNum))
            if crewNum == 'OOS':
                crewNum = 0
            duty = DBSession.query(DutyCrewCalendar).filter(DutyCrewCalendar.day == datetime.date(year, month, i+1)).one()
            duty.crewnumber = crewNum
    else:
        currentDate = datetime.date.today()
        year = currentDate.year
        month = currentDate.month
    
    monthName = calendar.month_name[month]
    #startDay is an integer representing the first day of the month
    #should be between 0 representing Sunday and 6 representing Saturday
    #days is the number of days in the month
    startDay, days = calendar.monthrange(year, month)
    startDay = (startDay +1)%7

    #crewNums is a list containing which crew is on for each day in the month
    crewNums = []
    for i in range(days):
        duty = DBSession.query(DutyCrewCalendar).filter(DutyCrewCalendar.day == datetime.date(year, month, i+1)).first()
        if duty:
            crewNums.append(duty.crewnumber)
        else:
            DBSession.add(
                          DutyCrewCalendar(
                                           day= datetime.date(year, month, i+1),
                                           crewnumber=0
                                           )
                          )
            crewNums.append('OOS')
            
    print("!!!!!!!!!!!!!!!!!!!{}".format(crewNums))
    return dict(
            title='Duty Crew Calendar',
            monthName=monthName,
            startDay=startDay,
            yearNum=year,
            monthNum=month,
            days=days,
            numOfCrews=numOfCrews,
            crewNums=crewNums,
            main=main,
            user=request.user
            )


@view_config(route_name='assign_duty_crew', renderer='templates/assign_duty_crew.pt',
             permission='admin')
def assign_duty_crew(request):
    main = get_renderer('templates/template.pt').implementation()
    allusers = DBSession.query(Users).all() 

    if 'form.submitted' in request.params:
        DBSession.query(DutyCrews).delete() #Delete all Duty Crews
        print("{}".format(request.params))
        allusernames = [auser.username for auser in allusers]
        for key,val in request.params.items():
            print("{}:{}".format(key,val))
            if key in allusernames:
                print("{}:{}".format(key,val))
                DBSession.add(
                              DutyCrews(
                                        crewnumber = int(val),
                                        username = key,
                                        )
                              )        
    all_user_records = []
    print("!!!!!!!!!!!")
    for some_user in allusers:
        user_record = DBSession.query(Users.fullname, Users.username, DutyCrews.crewnumber).\
                        outerjoin(DutyCrews).filter(DutyCrews.username == some_user.username).all()
        all_crews = [int(crew.crewnumber) for crew in user_record]
        all_user_records.append([some_user.fullname ,some_user.username,all_crews])
    print("!!!!!!!!!!!")
    print(all_user_records)

    return dict(
            title='Assign Duty Crew', 
            main=main,
            all_user_records=all_user_records,
            user=request.user
            )

@view_config(route_name='add_edit_announcements', renderer='templates/add_edit_announcements.pt',
             permission='admin')
def add_edit_announcements(request):
    main = get_renderer('templates/template.pt').implementation()
    announcementchosen = ''
    form = ''
    
    if 'form.submitted' in request.params:
        if request.params['option'] == 'New':
            announcement = Announcements('','','','','',)
            announcement.header = request.params['title']
            announcement.text = request.params['body']
            announcement.priority = int(request.params['privilege_level'])
            announcement.username = authenticated_userid(request)
            announcement.posted = datetime.datetime.today()
            DBSession.add(announcement)

        if request.params['option'] == 'Load':
            editannounce = request.params['editannouncement']
            announcement = DBSession.query(Announcements).filter_by(header = editannounce).first()
            announcement.text = request.params['body']
            announcement.priority = int(request.params['privilege_level'])
            DBSession.add(announcement)
        return HTTPFound(location = request.route_url('announcements'))

    if 'form.selected' in request.params:
        if request.params['form.selected'] == 'New':
            announcementchosen = ''
            announcement = Announcements('','','','','')
            form = 'New'
        if request.params['form.selected'] == 'Load':
            announcementchosen = request.params['selectedannouncement']
            announcement = DBSession.query(Announcements).filter_by(header=announcementchosen).first()
            form = 'Load'
        if request.params['form.selected'] == 'Delete':
            announcementchosen = request.params['selectedannouncement']
            announcement = DBSession.query(Announcements).filter_by(header=announcementchosen).first()
            DBSession.delete(announcement)
            return HTTPFound(location = request.route_url('announcements'))

    else:
        announcement = Announcements('','','','','')
        announcementchosen = ''
    
    allannouncements = DBSession.query(Announcements).all() 
    announcements = [announce.header for announce in allannouncements]
    
    all_privilege_levels = DBSession.query(Privileges).all()
    all_levels_list = [[level.privilegevalue, level.privilege] for level in all_privilege_levels]
    
    return dict(
            title='Add/Edit Announcements',
            main=main,
            announcements=announcements,
            announcement=announcement,
            privilege_levels=all_levels_list,
            form=form,
            announcementchosen=announcementchosen,
            user=request.user
            )

@view_config(route_name='add_edit_events', renderer='templates/add_edit_events.pt',
             permission='admin')
def add_edit_events(request):
    main = get_renderer('templates/template.pt').implementation()
    announcementchosen = ''
    form = ''
    monthdict = {'January': 1, 'February': 2, 'March': 3, 'April':4, 'May': 5, 'June': 6, 
        'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}

    if 'form.submitted' in request.params:
        if request.params['option'] == 'New':
            event = Events('','','','','','')
            event.name = request.params['title']
            event.notes = request.params['body']
            event.startdatetime = datetime.datetime(int(request.params['startyear']), monthdict[request.params['startmonth']],
                int(request.params['startday']), int(request.params['starthour']), int(request.params['startminute']), 0)
            event.enddatetime = datetime.datetime(int(request.params['endyear']), monthdict[request.params['startmonth']],
                int(request.params['endday']) , int(request.params['endhour']), int(request.params['endminute']), 0)
            event.location = request.params['location']
            event.privileges = request.params['privileges']
            DBSession.add(event)

        if request.params['option'] == 'Load':
            editevent = request.params['editevent']
            event = DBSession.query(Events).filter_by(name = editevent).first()
            event.notes = request.params['body']
            event.startdatetime = datetime.datetime(int(request.params['startyear']), monthdict[request.params['startmonth']],
                int(request.params['startday']), int(request.params['starthour']), int(request.params['startminute']), 0)
            event.enddatetime = datetime.datetime(int(request.params['endyear']), monthdict[request.params['startmonth']],
                int(request.params['endday']) , int(request.params['endhour']), int(request.params['endminute']), 0)
            DBSession.add(event)
            event.location = request.params['location']
            event.privileges = request.params['privileges']
        return HTTPFound(location = request.route_url('events'))
    
    if 'form.selected' in request.params:
        if request.params['form.selected'] == 'New':
            eventchosen = ''
            event = Events('','','','','','')
            form = 'New'
        if request.params['form.selected'] == 'Load':
            eventchosen = request.params['selectedevent']
            event = DBSession.query(Events).filter_by(name=eventchosen).first()
            form = 'Load'
        if request.params['form.selected'] == 'Delete':
            eventchosen = request.params['selectedevent']
            announcement = DBSession.query(Events).filter_by(name=eventchosen).first()
            DBSession.delete(event)
            return HTTPFound(location = request.route_url('events'))

    else:
        event = Events('','','','','','')
        eventchosen = ''
    
    allevents = DBSession.query(Events).all() 
    events = [eve.name for eve in allevents]
    yearlist = [year for year in range(datetime.datetime.now().year,datetime.datetime.now().year+30)]
    monthlist = ['January', 'February', 'March', 'April', 'May', 'June', 
        'July', 'August', 'September', 'October', 'November', 'December']
    daylist = [day for day in range(1,32)]
    hour = [hour for hour in range(0,24)]
    minute = [min for min in range(0,60)]
    minutelist = []
    hourlist = []

    for min in minute:
        if len(str(min))==1:
            min = '0'+str(min)
        minutelist.append(min)

    for min in hour:
        if len(str(min))==1:
            min = '0'+str(min)
        hourlist.append(min)

    return dict(
            title='Add/Edit Events', 
            yearlist=yearlist,
            monthlist=monthlist,
            daylist=daylist,
            hourlist=hourlist,
            minutelist=minutelist,
            main=main,
            user=request.user,
            events = events,
            event = event,
            form=form,
            eventchosen=eventchosen
            )

#@view_config(route_name='email', renderer='templates/email.pt')
#def email(request):
#    mainR = get_renderer('templates/template.pt').implementation()
#    mailer = get_mailer(request)
#    
#    message = Message(subject= "testing",
#                      sender= "laddbc@potsdam.edu",
#                      recipients= ["drbcladd@gmail.com"],
#                      body= "hopefully this thing works")
#    
#    mailer.send_immediately(message)
#    
#    return dict(
#             title='Email',
#             main=mainR,
#             user=request.user
#             )


@view_config(route_name='login', renderer='templates/login.pt')
@forbidden_view_config(renderer='templates/login.pt')
def login(request):
    main = get_renderer('templates/template.pt').implementation()
    login_url = request.route_url('login')
    referrer = request.url
    if referrer == login_url:
        referrer = '/member_info' # never use the login form itself as came_from
    came_from = request.params.get('came_from', referrer)
    message = ''
    login = ''
    password = ''
    if 'form.submitted' in request.params:
        login = request.params['login']
        password = request.params['password']
        password_query = DBSession.query(Users.password).filter(Users.username == login).first()
        if password_query:
            if password_query[0] == password:
                headers = remember(request, login)
                DBSession.add(
                              LoginIns(
                                       username = login,
                                       TSTAMP = datetime.datetime.now()
                              ))
                return HTTPFound(location = came_from,
                             headers = headers)
        message = 'Failed login'

    return dict(
        main=main,
        title='Login',
        message=message,
        url=request.application_url + '/login',
        came_from=came_from,
        login=login,
        password=password,
        user=request.user,
        )

@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(
            location=request.route_url('home'),
            headers=headers,
            )

@view_config(route_name='pictures', renderer='templates/pictures.pt')
def pictures(request):
    main = get_renderer('templates/template.pt').implementation()
    allpictures = []
    pictures = ''

    categories = DBSession.query(distinct(Pictures.category)).all()
    pictures = [DBSession.query(Pictures).filter(Pictures.category == cate[0]).first() for cate in categories]   
    allpictures = [[apicture.picture,apicture.description, apicture.category] for apicture in pictures] 

    return dict(title = 'Pictures',
				main = main,
				user=request.user,
				pictures = allpictures,
               )

@view_config(route_name='pictures_view', renderer='templates/pictures_view.pt')
def pictures_view(request):
    main = get_renderer('templates/template.pt').implementation()
    allpictures = []
    pictures = ''
    category = request.matchdict['category']

    if 'category' not in request.matchdict:
        return HTTPNotFound('No category passed in.')

    pictures = DBSession.query(Pictures).filter(Pictures.category == category).all()
    allpictures = [(apicture.picture,apicture.description, apicture.category) for apicture in pictures]
    
    return dict(title = 'Pictures',
				main = main,
				user=request.user,
				pictures = allpictures,
                category = category,
               )


@view_config(route_name='eboard', renderer='templates/eboard.pt')
def eboard(request):
    main = get_renderer('templates/template.pt').implementation()
    
    return dict(title='Our Executive Branch',
                main=main,
                user=request.user,
               )
    
@view_config(route_name='crew_chief_signup', renderer='templates/crew_chief_signup.pt')
def crew_chief_signup(request):
    main = get_renderer('templates/template.pt').implementation()
    year = 0
    month = 0
    if 'form.changedate' in request.params:
        if request.params['form.changedate'] == '<--':
            year = int(request.params['yearNum'])
            month = int(request.params['monthNum']) - 1
            if month < 1:
                month = 12
                year = year - 1
        if request.params['form.changedate'] == '-->':
            year = int(request.params['yearNum'])
            month = int(request.params['monthNum']) + 1
            if month > 12:
                month = 1
                year = year + 1
    else:
        currentDate = datetime.date.today()
        year = currentDate.year
        month = currentDate.month

    monthName = calendar.month_name[month]
    startDay, days = calendar.monthrange(year, month)
    startDay = (startDay +1)%7
    return dict(title='Crew Chief Sign-Up',
                monthName=monthName,
                startDay=startDay,
                yearNum=year,
                monthNum=month,
                days=days,
                main=main,
                user=request.user,
               )
    
@view_config(route_name='edit_eboard', renderer='templates/edit_eboard.pt')
def edit_eboard(request):
    main = get_renderer('templates/template.pt').implementation()
    eboard = DBSession.query(EboardPositions).\
                filter(not EboardPositions.username == '').\
                join(Users)\
                .all()
    
    
    return dict(title='Edit Eboard',
                main=main,
                user=request.user,
               )
    
@view_config(route_name='check_login', renderer='templates/check_login.pt')
def check_logins(request):
    main = get_renderer('templates/template.pt').implementation()
    logins = DBSession.query(LoginIns).order_by(LoginIns.TSTAMP.desc()).all()
    all_logins = [[log.username , log.TSTAMP] for log in logins]
    
    return dict(title='Check Logins',
                main=main,
                user=request.user,
                all_logins = all_logins,
               )

conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_rescueweb_db" script
    to initialize your database tables.  Check your virtual 
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

def get_username(request):
    """Returns the logged in user or None if no user is logged in.

    This avoid the problem of dereferecing `None' if no user is logged in.

    """
    if request.user:
        return request.user.username
    else:
        return ''

def get_privilege_value(request):
    """Returns the privilege level of the user or 0 if no one is logged in"""
    if request.user:
        return request.user.privilegevalue
    else:
        return 0
