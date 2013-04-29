import calendar
import datetime
import random


from pyramid.response import Response
from pyramid.view import view_config
from pyramid.renderers import get_renderer

from sqlalchemy.exc import DBAPIError

from pyramid_mailer import get_mailer
from pyramid_mailer.message import Message


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
    )

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
    page = DBSession.query(Announcements).order_by(Announcements.posted.desc()).all()
    headers = [column.name for column in page[0].__table__.columns]

    return dict(
            title='Announcements', 
            main=main,
            announcements=page, headers=headers,
            user=request.user)
    
@view_config(route_name='events', renderer='templates/events.pt')
def eventsV(request):
    main = get_renderer('templates/template.pt').implementation()
    ev = DBSession.query(Events).all()

    return dict(
            title='Events', 
            main=main,
            user=request.user,
            ev=ev
            )

@view_config(route_name='pictures', renderer='templates/pictures.pt')
def pictures(request):
    main = get_renderer('templates/template.pt').implementation()

    return dict(title='Pictures',
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

    return dict(
            title='Meeting Minutes',
            main=main,
            user=request.user
            )

@view_config(route_name='member_info', renderer='templates/member_info.pt',
             permission='Member')
def member_info(request):
    main = get_renderer('templates/template.pt').implementation()

    return dict(
            title='Member Information',
            main=main,
            user=request.user
            )
    
@view_config(route_name='standbys', renderer='templates/standbys.pt',
             permission='Member')
def standbys(request):
    main = get_renderer('templates/template.pt').implementation()

    return dict(
            title='Stand-Bys', 
            main=main,
            user=request.user
            )

@view_config(name='standby_dates.json', renderer='json')
def standby_dates(request):
    """Serves up Standby dates via JSON back to the calendar. 
    
    This function is called when the calendar is first loaded. The calendar uses
    this information to highlight days Standbys are scheduled.

    """
    standby_query = DBSession.query(StandBy).all()

    return [ 
        (
            '{}/{}/{}'.format(
                standby.startdatetime.month, 
                standby.startdatetime.day,
                standby.startdatetime.year
                             ),
            '{}/{}/{}'.format(
                standby.enddatetime.month,
                standby.enddatetime.day, 
                standby.enddatetime.year
                             )
        ) for standby in standby_query 
           ]

@view_config(name='standby_info.json', renderer='json')
def standby_information(request):
    """Serves up information about Standbys on a particular date via JSON"""
    if 'date' not in request.POST:
        # No date was sent
        return 'No Date'

    # Grab the date from the AJAX request
    month, day, year = request.POST['date'].split('/')
    standby_date = datetime.datetime(int(year), int(month), int(day))
    standby_query = DBSession.query(StandBy).filter(StandBy.startdatetime == standby_date)

    # Return all of the Standby dates occurring on this date
    return [
        (
            standby.event,
            standby.location,
            standby.notes,
            str(standby.startdatetime),
            str(standby.enddatetime),
        ) for standby in standby_query 
           ]

@view_config(route_name='duty_crew_calendar',
             renderer='templates/duty_crew_calendar.pt', permission='Member')
def duty_crew_calendar(request):
    main = get_renderer('templates/template.pt').implementation()
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
            days=days,
            main=main,
            user=request.user
            )

@view_config(route_name='coverage', renderer='templates/coverage.pt',
             permission='Member')
def coverage(request):
    main = get_renderer('templates/template.pt').implementation()
    return dict(
            title='Coverage Requests',
            main=main,
            user=request.user
            )
    
@view_config(route_name='add_user', renderer='templates/add_user.pt',
             permission='admin')
def add_user(request):
    main = get_renderer('templates/template.pt').implementation()

    if 'form.submitted' in request.params:
        newuser = Users('','','','','','','','','','','','','','','','','','','')
        newuser.username = request.params['username']
        newuser.password = request.params['password']
        newuser.firstname = request.params['firstname']
        newuser.middlename = request.params['middlename']
        newuser.lastname = request.params['lastname']
        newuser.birthday = datetime.date(int(request.params['year']),int(request.params['month']),int(request.params['day']))
        newuser.street = request.params['street']
        newuser.city = request.params['city']
        newuser.state = request.params['state']
        newuser.zipcode = request.params['zipcode']
        newuser.residence = request.params['residence']
        newuser.roomnumber = request.params['roomnumber']
        newuser.phonenumber = request.params['phonenumber']
        newuser.email = request.params['email']
        
        list = DBSession.query(Privileges).filter(Privileges.privilege == request.params['privileges']).one()
        newuser.privileges = list.privilegevalue
        list = DBSession.query(TrainingLevel).filter(TrainingLevel.traininglevel == request.params['trainingvalue']).one()
        newuser.trainingvalue = list.trainingvalue
        list = DBSession.query(AdministrativeStatus).filter(AdministrativeStatus.status == request.params['administrativevalue']).one()
        newuser.administrativevalue = list.administrativevalue
        list = DBSession.query(OperationalStatus).filter(OperationalStatus.status == request.params['operationalvalue']).one()
        newuser.operationalvalue = list.operationalvalue
        
        DBSession.add(newuser)
            
    Options = DBSession.query(Privileges).all()
    privilegesOptions = [option.privilege for option in Options]
    Options = DBSession.query(TrainingLevel).all()
    trainingOptions = [option.traininglevel for option in Options]
    Options = DBSession.query(AdministrativeStatus).all()
    administrativeOptions = [option.status for option in Options]
    Options = DBSession.query(OperationalStatus).all()
    operationalOptions = [option.status for option in Options]
    
    return dict(
            title='Add User',
            main=main,
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
    if 'userselected' in request.params:
        userselected = request.params['userselected']
    else:
        userselected = ''
    
    if 'form.submitted' in request.params:
        userselected = request.params['userselected']
        edited_user = DBSession.query(Users).filter_by(username=userselected).first()
        edited_user.username = request.params['username']
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
        list = DBSession.query(Privileges).filter(Privileges.privilege == request.params['privileges']).one()
        edited_user.privileges = list.privilegevalue
        list = DBSession.query(TrainingLevel).filter(TrainingLevel.traininglevel == request.params['trainingvalue']).one()
        edited_user.trainingvalue = list.trainingvalue
        list = DBSession.query(AdministrativeStatus).filter(AdministrativeStatus.status == request.params['administrativevalue']).one()
        edited_user.administrativevalue = list.administrativevalue
        list = DBSession.query(OperationalStatus).filter(OperationalStatus.status == request.params['operationalvalue']).one()
        edited_user.operationalvalue = list.operationalvalue
        DBSession.add(edited_user)
        
    if 'form.selected' in request.params:
        userselected = request.params['selecteduser']
        edited_user = DBSession.query(Users).filter_by(username=userselected).first()
    else:
        userselected = ''
        edited_user = Users('','','','','','','','','','','','','','','','','','','')

    Options = DBSession.query(Privileges).all()
    privilegesOptions = [option.privilege for option in Options]
    Options = DBSession.query(TrainingLevel).all()
    trainingOptions = [option.traininglevel for option in Options]
    Options = DBSession.query(AdministrativeStatus).all()
    administrativeOptions = [option.status for option in Options]
    Options = DBSession.query(OperationalStatus).all()
    operationalOptions = [option.status for option in Options]
    
    allusers = DBSession.query(Users).order_by(Users.username).all() 
    allusernames = [auser.username for auser in allusers]
    
    return dict(
            title='Edit User',
            main=main,
            userselected=userselected,
            edited_user=edited_user,
            users=allusernames,
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

    return dict(
            title='Add/Edit documents',
            main=main,
            user=request.user
            )

@view_config(route_name='add_edit_minutes', renderer='templates/add_edit_minutes.pt',
             permission='admin')
def editmeetingminutes(request):
    main = get_renderer('templates/template.pt').implementation()

    return dict(
            title='Add/Edit Meeting Minutes',
            main=main,
            user=request.user
            )

@view_config(route_name='add_edit_pictures', renderer='templates/add_edit_pictures.pt',
             permission='admin')
def add_edit_pictures(request):
    main = get_renderer('templates/template.pt').implementation()

    return dict(
            title='Add/Edit Pictures',
            main=main,
            user=request.user
            )

@view_config(route_name='edit_portable_numbers', renderer='templates/edit_portable_numbers.pt',
             permission='admin')
def edit_portable_numbers(request):
    main = get_renderer('templates/template.pt').implementation()
    
    if 'form.submitted' in request.params:
        allusers = DBSession.query(Users).order_by(Users.username).all() 
        for changeuser in allusers:
            i = int(request.params[changeuser.username])
            if i:
                changeuser.portablenumber = i
                DBSession.add(changeuser)
                print("should have Changed")
            print(i)
        
    allusers = DBSession.query(Users).order_by(Users.username).all() 
    allusernames = [[auser.username , auser.portablenumber] for auser in allusers]
    
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
    allusers = DBSession.query(Users).order_by(Users.username).all() 
    allusernames = [auser.username for auser in allusers]
    return dict(
            title='Add/Edit Certifications',
            main=main,
            allusers = allusernames,
            user=request.user
            )
    
@view_config(route_name='add_edit_standby', renderer='templates/add_edit_standby.pt',
             permission='admin')
def add_edit_standby(request):
    main = get_renderer('templates/template.pt').implementation()

    return dict(title='Add/Edit Standby',
            main=main,
            user=request.user
            )

@view_config(route_name='edit_duty_crew', renderer='templates/edit_duty_crew.pt',
             permission='admin')
def edit_duty_crew(request):
    main = get_renderer('templates/template.pt').implementation()
     
    return dict(
            title='Edit Duty Crew', 
            main=main,
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
            announcement.priority = 0
            announcement.username = authenticated_userid(request)
            announcement.posted = datetime.datetime.today()
            DBSession.add(announcement)

        if request.params['option'] == 'Load':
            editannounce = request.params['editannouncement']
            announcement = DBSession.query(Announcements).filter_by(header = editannounce).first()
            announcement.text = request.params['body']
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
    announcements = [announcement.header for announcement in allannouncements]
    
    return dict(
            title='Add/Edit Announcements',
            main=main,
            announcements=announcements,
            announcement=announcement,
            form=form,
            announcementchosen=announcementchosen,
            user=request.user
            )

@view_config(route_name='add_edit_events', renderer='templates/add_edit_events.pt',
             permission='admin')
def add_edit_events(request):
    main = get_renderer('templates/template.pt').implementation()

    return dict(
            title='Add/Edit Events', 
            main=main,
            user=request.user
            )
@view_config(route_name='email', renderer='templates/email.pt',
             permission='admin')
def email(request):
    main = get_renderer('templates/template.pt').implementation()
    mailer = get_mailer(request)
    
    message = Message(subject = "testing",
                      sender = "rosejp194@potsdam.edu",
                      recipients = ["jeremy.rose09@gmail.com"],
                      body = "hopefully this thing works")
    #mailer.send(message)
    
    return dict(
             title = 'Email',
             main = main,
             user = request.user
             )


@view_config(route_name='login', renderer='templates/login.pt')
@forbidden_view_config(renderer='templates/login.pt')
def login(request):
    main = get_renderer('templates/template.pt').implementation()
    login_url = request.route_url('login')
    referrer = request.url
    if referrer == login_url:
        referrer = '/' # never use the login form itself as came_from
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
