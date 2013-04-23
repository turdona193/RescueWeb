import calendar
import datetime


from pyramid.response import Response
from pyramid.view import view_config
from pyramid.renderers import get_renderer

from sqlalchemy.exc import DBAPIError
from .security import USERS

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
    events,
    users,
    emtcert,
    certifications,
    privileges,
    operationalstatus,
    administrativestatus,
    eboardpositions,
    traininglevel,
    weblinks,
    )
@view_config(route_name='home', renderer='templates/home.pt')
def home(request):
    main = get_renderer('templates/template.pt').implementation()
    page = DBSession.query(Page).filter_by(name='Home').first()

    return dict(title='Home', main=main , page = page,
                logged_in=authenticated_userid(request))

@view_config(route_name='history', renderer='templates/history.pt')
def history(request):
    main = get_renderer('templates/template.pt').implementation()
    page = DBSession.query(Page).filter_by(name='History').first()
    return dict(title = 'History', main = main , page = page,
                logged_in=authenticated_userid(request))

@view_config(route_name='personnel', renderer='templates/personnel.pt')
def personnel(request):
    main = get_renderer('templates/template.pt').implementation()
    page = DBSession.query(users).all()
    
    headers = [column.name for column in page[0].__table__.columns]
    return dict(title = 'Personnel', main = main, personnel = page, headers = headers,
                logged_in=authenticated_userid(request))


@view_config(route_name='announcements', renderer='templates/announcements.pt')
def announcements(request):
    main = get_renderer('templates/template.pt').implementation()
    page = DBSession.query(Announcements).order_by(Announcements.posted.desc()).all()
    headers = [column.name for column in page[0].__table__.columns]
    return dict(title = 'Announcements', main = main,  announcements = page, headers = headers,
                logged_in=authenticated_userid(request))
    
@view_config(route_name='events', renderer='templates/events.pt')
def eventsV(request):
    main = get_renderer('templates/template.pt').implementation()
    ev = DBSession.query(events).all()
    return dict(title = 'Events', main = main,
                logged_in=authenticated_userid(request),
                ev = ev)


@view_config(route_name='pictures', renderer='templates/pictures.pt')
def pictures(request):
    main = get_renderer('templates/template.pt').implementation()
    return dict(title = 'Pictures', main = main,
                logged_in=authenticated_userid(request))   


@view_config(route_name='join', renderer='templates/join.pt')
def join(request):
    main = get_renderer('templates/template.pt').implementation()
    page = DBSession.query(Page).filter_by(name='Join').first()
    return dict(title = 'How to Join', main = main , page = page,
                logged_in=authenticated_userid(request))
    

    
@view_config(route_name='contact', renderer='templates/contact.pt')
def contact(request):
    main = get_renderer('templates/template.pt').implementation()
    page = DBSession.query(Page).filter_by(name='ContactUs').first()
    return dict(title = 'Contact Us', main = main, page = page,
                logged_in=authenticated_userid(request))
    
@view_config(route_name='links', renderer='templates/links.pt')
def links(request):
    main = get_renderer('templates/template.pt').implementation()
    page = DBSession.query(weblinks).all()
    
    headers = [column.name for column in page[0].__table__.columns]
    return dict(title = 'Links', main = main, links = page, header = headers,
                logged_in=authenticated_userid(request))


@view_config(route_name='documents', renderer='templates/documents.pt',
             permission = 'Member')
def documents(request):
    main = get_renderer('templates/template.pt').implementation()
    page = DBSession.query(Documents).all()
    headers = [column.name for column in page[0].__table__.columns]

    
    return dict(title = 'Squad Documents', main = main,page = page, header = headers,
                logged_in=authenticated_userid(request))

@view_config(route_name='minutes', renderer='templates/minutes.pt',
             permission = 'Member')
def minutes(request):
    main = get_renderer('templates/template.pt').implementation()
    return dict(title = 'Meeting Minutes', main = main,
                logged_in=authenticated_userid(request))

@view_config(route_name='memberinfo', renderer='templates/memberinfo.pt',
             permission = 'Member')
def memberinfo(request):
    main = get_renderer('templates/template.pt').implementation()
    return dict(title = 'Member Information', main = main,
                logged_in=authenticated_userid(request))
    


@view_config(route_name='standbys', renderer='templates/standbys.pt',
             permission = 'Member')
def standbys(request):
    main = get_renderer('templates/template.pt').implementation()
    return dict(title = 'Stand-Bys', main = main,
                logged_in=authenticated_userid(request)) 


@view_config(route_name='duty_crew_calendar',
             renderer='templates/duty_crew_calendar.pt', permission = 'Member')
def duty_crew_calendar(request):
    main = get_renderer('templates/template.pt').implementation()
    currentDate = datetime.date.today()
    year = currentDate.year
    month = currentDate.month
    monthName = calendar.month_name[month]
    startDay, days = calendar.monthrange(year, month)
    startDay = (startDay +1)%7
    return dict(title = 'Duty Crew Calendar',
                monthName = monthName,
                startDay = startDay,
                days = days,
                main = main,
                logged_in=authenticated_userid(request))

    
@view_config(route_name='coverage', renderer='templates/coverage.pt',
             permission = 'Member')
def coverage(request):
    main = get_renderer('templates/template.pt').implementation()
    return dict(title = 'Coverage Requests', main = main,
                logged_in=authenticated_userid(request))
    
   

    
@view_config(route_name='adduser', renderer='templates/adduser.pt',
             permission = 'admin')
def adduser(request):
    main = get_renderer('templates/template.pt').implementation()
    headers = [column.name for column in users.__table__.columns][:-5]

    if 'form.submitted' in request.params:
        newuser = users('','','','','','','','','','','','','','','','','','','')
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
        newuser.privileges = request.params['privileges']
        newuser.trainingvalue = request.params['trainingvalue']
        newuser.administrativevalue = request.params['administrativevalue']
        newuser.operationalvalue = request.params['operationalvalue']
        DBSession.add(newuser)
    
    Options = DBSession.query(privileges).all()
    privilegesOptions = [option.privilege for option in Options]
    Options = DBSession.query(traininglevel).all()
    trainingOptions = [option.traininglevel for option in Options]
    Options = DBSession.query(administrativestatus).all()
    administrativeOptions = [option.status for option in Options]
    Options = DBSession.query(operationalstatus).all()
    operationalOptions = [option.status for option in Options]
    
    return dict(title = 'Add User',
                main = main,
                headers = headers,
                privilegesOptions = privilegesOptions,
                trainingOptions = trainingOptions,
                administrativeOptions = administrativeOptions,
                operationalOptions = operationalOptions,
                logged_in=authenticated_userid(request)
                )

@view_config(route_name='edituser', renderer='templates/edituser.pt',
             permission = 'admin')
def edituser(request):
    main = get_renderer('templates/template.pt').implementation()
    userselected = ''
    
    if 'form.submitted' in request.params:
        editeduser = users('','','','','','','','','','','','','','','','','','','')
        editeduser.username = request.params['username']
        editeduser.password = request.params['password']
        editeduser.firstname = request.params['firstname']
        editeduser.middlename = request.params['middlename']
        editeduser.lastname = request.params['lastname']
        editeduser.birthday = datetime.date(int(request.params['year']),int(request.params['month']),int(request.params['day']))
        editeduser.street = request.params['street']
        editeduser.city = request.params['city']
        editeduser.state = request.params['state']
        editeduser.zipcode = request.params['zipcode']
        editeduser.residence = request.params['residence']
        editeduser.roomnumber = request.params['roomnumber']
        editeduser.phonenumber = request.params['phonenumber']
        editeduser.email = request.params['email']
        editeduser.privileges = request.params['privileges']
        editeduser.trainingvalue = request.params['trainingvalue']
        editeduser.administrativevalue = request.params['administrativevalue']
        editeduser.operationalvalue = request.params['operationalvalue']
        DBSession.add(editeduser)
        
    if 'form.selected' in request.params:
        userselected = request.params['selecteduser']
        editeduser  = DBSession.query(users).filter_by(username=userselected).first()
    else:
        userselected = ''
        editeduser = users('','','','','','','','','','','','','','','','','','','')
    
    Options = DBSession.query(privileges).all()
    privilegesOptions = [option.privilege for option in Options]
    Options = DBSession.query(traininglevel).all()
    trainingOptions = [option.traininglevel for option in Options]
    Options = DBSession.query(administrativestatus).all()
    administrativeOptions = [option.status for option in Options]
    Options = DBSession.query(operationalstatus).all()
    operationalOptions = [option.status for option in Options]
    
    allusers = DBSession.query(users).order_by(users.username).all() 
    allusernames = [auser.username for auser in allusers]
    
    return dict(title = 'Edit User',
                main = main,
                userselected = userselected,
                editeduser = editeduser,
                users = allusernames,
                privilegesOptions = privilegesOptions,
                trainingOptions = trainingOptions,
                administrativeOptions = administrativeOptions,
                operationalOptions = operationalOptions,
                logged_in=authenticated_userid(request))

@view_config(route_name='deleteuser', renderer='templates/deleteuser.pt',
             permission = 'admin')
def deleteuser(request):
    main = get_renderer('templates/template.pt').implementation()
    return dict(title = 'Delete User', main = main,
                logged_in=authenticated_userid(request))
    

@view_config(route_name='editpages', renderer='templates/editpages.pt',
             permission = 'admin')
def editpages(request):
    main = get_renderer('templates/template.pt').implementation()
    pagenames = ['Home' , 'History' ,'Join', 'ContactUs' ]    
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
        
    return dict(title = 'Edit Pages', 
                main = main, 
                page = page, 
                pagenames = pagenames, 
                pageselected = pageselected,
                logged_in=authenticated_userid(request))

@view_config(route_name='addeditlinks', renderer='templates/addeditlinks.pt',
             permission = 'admin')
def addeditlinks(request):
    main = get_renderer('templates/template.pt').implementation()
    return dict(title = 'Add/Edit Links', main = main,
                logged_in=authenticated_userid(request))

@view_config(route_name='addeditdocuments', renderer='templates/addeditdocuments.pt',
             permission = 'admin')
def addeditdocuments(request):
    main = get_renderer('templates/template.pt').implementation()
    return dict(title = 'Add/Edit documents', main = main,
                logged_in=authenticated_userid(request))

@view_config(route_name='addeditminutes', renderer='templates/addeditminutes.pt',
             permission = 'admin')
def editmeetingminutes(request):
    main = get_renderer('templates/template.pt').implementation()
    return dict(title = 'Add/Edit Meeting Minutes', main = main,
                logged_in=authenticated_userid(request))

@view_config(route_name='addeditpictures', renderer='templates/addeditpictures.pt',
             permission = 'admin')
def addeditpictures(request):
    main = get_renderer('templates/template.pt').implementation()
    return dict(title = 'Add/Edit Pictures', main = main,
                logged_in=authenticated_userid(request))




@view_config(route_name='editportableNumbers', renderer='templates/editportableNumbers.pt',
             permission = 'admin')
def editportableNumbers(request):
    main = get_renderer('templates/template.pt').implementation()
    return dict(title = 'Edit Portable Numbers', main = main,
                logged_in=authenticated_userid(request))

@view_config(route_name='addeditcertifications', renderer='templates/addeditcertifications.pt',
             permission = 'admin')
def addeditcertifications(request):
    main = get_renderer('templates/template.pt').implementation()
    return dict(title = 'Add/Edit Certifications', main = main,
                logged_in=authenticated_userid(request))
    
@view_config(route_name='addeditstandby', renderer='templates/addeditstandby.pt',
             permission = 'admin')
def addeditstandby(request):
    main = get_renderer('templates/template.pt').implementation()
    return dict(title = 'Add/Edit Standby', main = main,
                logged_in=authenticated_userid(request))

@view_config(route_name='editdutycrew', renderer='templates/editdutycrew.pt',
             permission = 'admin')
def editdutycrew(request):
    main = get_renderer('templates/template.pt').implementation()
    return dict(title = 'Edit Duty Crew', main = main,
                logged_in=authenticated_userid(request))

@view_config(route_name='addeditannouncements', renderer='templates/addeditannouncements.pt',
             permission = 'admin')
def addeditannouncements(request):
    main = get_renderer('templates/template.pt').implementation()
    announcementchosen = ''
    form = ''
    
    if 'form.submitted' in request.params:
        if request.params['option'] == 'New':
            announcement = Announcements('','','','', '',' ')
            announcement.header = request.params['title']
            announcement.text  = request.params['body']
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
            announcement = Announcements('','','','', '','')
            form = 'New'
        if request.params['form.selected'] == 'Load':
            announcementchosen = request.params['selectedannouncement']
            announcement  = DBSession.query(Announcements).filter_by(header=announcementchosen).first()
            form = 'Load'
        if request.params['form.selected'] == 'Delete':
            announcementchosen = request.params['selectedannouncement']
            announcement = DBSession.query(Announcements).filter_by(header=announcementchosen).first()
            DBSession.delete(announcement)
            return HTTPFound(location = request.route_url('announcements'))

    else:
        announcement = Announcements('','','','', '',' ')
        announcementchosen = ''
    
    allannouncements = DBSession.query(Announcements).all() 
    announcements = [announcement.header for announcement in allannouncements]
    
    return dict(title='Add/Edit Announcements',
                main=main,
                announcements=announcements,
                announcement=announcement,
                form=form,
                announcementchosen=announcementchosen,
                logged_in=authenticated_userid(request))



@view_config(route_name='addeditevents', renderer='templates/addeditevents.pt',
             permission='admin')
def addeditevents(request):
    main = get_renderer('templates/template.pt').implementation()
    return dict(title='Add/Edit Events', main=main,
                logged_in=authenticated_userid(request))



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
        if DBSession.query(users.username).filter(users.username.like(login)).count() > 0:
            password_query = DBSession.query(users.password).filter(users.username == login).first()[0]
            if password_query == password:
                headers = remember(request, login)
                return HTTPFound(location = came_from,
                             headers = headers)
        message = 'Failed login'

    return dict(
        main = main,
        title = 'Login',
        message = message,
        url = request.application_url + '/login',
        came_from = came_from,
        login = login,
        password = password,
        logged_in=authenticated_userid(request))

@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(location = request.route_url('home'),
                     headers = headers,
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

