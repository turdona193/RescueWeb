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
    
@view_config(route_name='contact', renderer='templates/contact.pt')
def contact(request):
    main = get_renderer('templates/template.pt').implementation()
    page = DBSession.query(Page).filter_by(name='ContactUs').first()
    return dict(title = 'Personnel', main = main, page = page,
                logged_in=authenticated_userid(request))
    
@view_config(route_name='links', renderer='templates/links.pt')
def links(request):
    main = get_renderer('templates/template.pt').implementation()
    page = DBSession.query(weblinks).all()
    
    headers = [column.name for column in page[0].__table__.columns]
    return dict(title = 'Links', main = main, links = page, header = headers,
                logged_in=authenticated_userid(request))

@view_config(route_name='duty_crew_calendar', renderer='templates/duty_crew_calendar.pt',
             permission = 'Member')
def duty_crew_calendar(request):
    main = get_renderer('templates/template.pt').implementation()

    import calendar
    import datetime

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

@view_config(route_name='announcements', renderer='templates/announcements.pt')
def announcements(request):
    main = get_renderer('templates/template.pt').implementation()
    page = DBSession.query(Announcements).all()

    
    headers = [column.name for column in page[0].__table__.columns]
    return dict(title = 'Announcements', main = main,  announcements = page, headers = headers,
                logged_in=authenticated_userid(request))

@view_config(route_name='join', renderer='templates/join.pt')
def join(request):
    main = get_renderer('templates/template.pt').implementation()
    page = DBSession.query(Page).filter_by(name='Join').first()
    return dict(title = 'Join', main = main , page = page,
                logged_in=authenticated_userid(request))
    
@view_config(route_name='events', renderer='templates/events.pt')
def events(request):
    main = get_renderer('templates/template.pt').implementation()
    return dict(title = 'Events', main = main,
                logged_in=authenticated_userid(request))

@view_config(route_name='pictures', renderer='templates/pictures.pt')
def pictures(request):
    main = get_renderer('templates/template.pt').implementation()
    return dict(title = 'Pictures', main = main,
                logged_in=authenticated_userid(request))
    
@view_config(route_name='standbys', renderer='templates/standbys.pt')
def standbys(request):
    main = get_renderer('templates/template.pt').implementation()
    return dict(title = 'Stand-Bys', main = main,
                logged_in=authenticated_userid(request)) 
    
@view_config(route_name='coverage', renderer='templates/coverage.pt')
def coverage(request):
    main = get_renderer('templates/template.pt').implementation()
    return dict(title = 'Coverage Requests', main = main,
                logged_in=authenticated_userid(request))
    
@view_config(route_name='minutes', renderer='templates/minutes.pt')
def minutes(request):
    main = get_renderer('templates/template.pt').implementation()
    return dict(title = 'Meeting Minutes', main = main,
                logged_in=authenticated_userid(request))
    
@view_config(route_name='documents', renderer='templates/documents.pt')
def documents(request):
    main = get_renderer('templates/template.pt').implementation()
    page = DBSession.query(Documents).all()
    headers = [column.name for column in page[0].__table__.columns]

    
    return dict(title = 'Squad Documents', main = main,page = page, header = headers,
                logged_in=authenticated_userid(request))
    
@view_config(route_name='adduser', renderer='templates/adduser.pt',
             permission = 'admin')
def adduser(request):
    main = get_renderer('templates/template.pt').implementation()
    headers = [column.name for column in users.__table__.columns][:-5]

    if 'form.submitted' in request.params:
        print("hello")
        
    privilegesOptions = DBSession.query(privileges.privilege).all()
    trainingOptions = DBSession.query(traininglevel.traininglevel).all()
    administrativeOptions = DBSession.query(administrativestatus.status).all()
    operationalOptions = DBSession.query(operationalstatus.status).all()

    
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
    return dict(title = 'Edit User', main = main,
                logged_in=authenticated_userid(request))

@view_config(route_name='deleteuser', renderer='templates/deleteuser.pt',
             permission = 'admin')
def deleteuser(request):
    main = get_renderer('templates/template.pt').implementation()
    return dict(title = 'Delete User', main = main,
                logged_in=authenticated_userid(request))

@view_config(route_name='editportableNumbers', renderer='templates/editportableNumbers.pt',
             permission = 'admin')
def editportableNumbers(request):
    main = get_renderer('templates/template.pt').implementation()
    return dict(title = 'Portable Numbers', main = main,
                logged_in=authenticated_userid(request))

@view_config(route_name='addannouncements', renderer='templates/addannouncements.pt',
             permission = 'admin')
def addannouncements(request):
    main = get_renderer('templates/template.pt').implementation()
    return dict(title = 'Add Announcements', main = main,
                logged_in=authenticated_userid(request))

view_config(route_name='addevents', renderer='templates/addevents.pt',
             permission = 'admin')
def addevents(request):
    main = get_renderer('templates/template.pt').implementation()
    return dict(title = 'Add Events', main = main,
                logged_in=authenticated_userid(request))

view_config(route_name='addstandby', renderer='templates/addstandby.pt',
             permission = 'admin')
def addstandby(request):
    main = get_renderer('templates/template.pt').implementation()
    return dict(title = 'Add Standby', main = main,
                logged_in=authenticated_userid(request))

view_config(route_name='editdutycrew', renderer='templates/editdutycrew.pt',
             permission = 'admin')
def editdutycrew(request):
    main = get_renderer('templates/template.pt').implementation()
    return dict(title = 'Edit Duty Crew', main = main,
                logged_in=authenticated_userid(request))
view_config(route_name='editcertifications', renderer='templates/editcertifications.pt',

             permission = 'admin')
def editcertifications(request):
    main = get_renderer('templates/template.pt').implementation()
    return dict(title = 'Edit Certifications', main = main,
                logged_in=authenticated_userid(request))

view_config(route_name='editannouncements', renderer='templates/editannouncements.pt',
             permission = 'admin')
def editannouncements(request):
    main = get_renderer('templates/template.pt').implementation()
    return dict(title = 'Edit Announcements', main = main,
                logged_in=authenticated_userid(request))

view_config(route_name='editpages', renderer='templates/editpages.pt',
             permission = 'admin')
def editpages(request):
    main = get_renderer('templates/template.pt').implementation()
    return dict(title = 'Edit Pages', main = main,
                logged_in=authenticated_userid(request))

view_config(route_name='editlinks', renderer='templates/editlinks.pt',
             permission = 'admin')
def editlinks(request):
    main = get_renderer('templates/template.pt').implementation()
    return dict(title = 'Edit Links', main = main,
                logged_in=authenticated_userid(request))

view_config(route_name='editdocuments', renderer='templates/editdocuments.pt',
             permission = 'admin')
def editdocuments(request):
    main = get_renderer('templates/template.pt').implementation()
    return dict(title = 'Edit documents', main = main,
                logged_in=authenticated_userid(request))

view_config(route_name='editpictures', renderer='templates/editpictures.pt',
             permission = 'admin')
def editpictures(request):
    main = get_renderer('templates/template.pt').implementation()
    return dict(title = 'Edit Pictures', main = main,
                logged_in=authenticated_userid(request))

view_config(route_name='editmeetingminutes', renderer='templates/editmeetingminutes.pt',
             permission = 'admin')
def editmeetingminutes(request):
    main = get_renderer('templates/template.pt').implementation()
    return dict(title = 'Edit Meeting Minutes', main = main,
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
        if USERS.get(login) == password:
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

