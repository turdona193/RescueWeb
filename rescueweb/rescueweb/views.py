import calendar
import datetime
import random


from pyramid.response import Response
from pyramid.view import view_config
from pyramid.renderers import get_renderer

from sqlalchemy.exc import DBAPIError

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
    page = DBSession.query(Users).all()
    
    headers = [column.name for column in page[0].__table__.columns]

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
    return dict(title = 'Events', main = main,
                user=request.user,
                ev = ev)


@view_config(route_name='pictures', renderer='templates/pictures.pt')
def pictures(request):
    main = get_renderer('templates/template.pt').implementation()
    return dict(title = 'Pictures', main = main,
                user=request.user)   


@view_config(route_name='join', renderer='templates/join.pt')
def join(request):
    main = get_renderer('templates/template.pt').implementation()
    page = DBSession.query(Page).filter_by(name='Join').first()
    return dict(title = 'How to Join', main = main , page = page,
                user=request.user)
    

    
@view_config(route_name='contact', renderer='templates/contact.pt')
def contact(request):
    main = get_renderer('templates/template.pt').implementation()
    page = DBSession.query(Page).filter_by(name='ContactUs').first()
    return dict(title = 'Contact Us', main = main, page = page,
                user=request.user)
    
@view_config(route_name='links', renderer='templates/links.pt')
def links(request):
    main = get_renderer('templates/template.pt').implementation()
    page = DBSession.query(WebLinks).all()
    
    headers = [column.name for column in page[0].__table__.columns]
    return dict(title = 'Links', main = main, links = page, header = headers,
                user=request.user)


@view_config(route_name='documents', renderer='templates/documents.pt',
             permission = 'Member')
def documents(request):
    main = get_renderer('templates/template.pt').implementation()
    page = DBSession.query(Documents).all()
    headers = [column.name for column in page[0].__table__.columns]

    
    return dict(title = 'Squad Documents', main = main,page = page, header = headers,
                user=request.user)

@view_config(route_name='minutes', renderer='templates/minutes.pt',
             permission = 'Member')
def minutes(request):
    main = get_renderer('templates/template.pt').implementation()
    return dict(title = 'Meeting Minutes', main = main,
                user=request.user)

@view_config(route_name='memberinfo', renderer='templates/memberinfo.pt',
             permission = 'Member')
def memberinfo(request):
    main = get_renderer('templates/template.pt').implementation()
    return dict(title = 'Member Information', main = main,
                user=request.user)
    


@view_config(route_name='standbys', renderer='templates/standbys.pt',
             permission = 'Member')
def standbys(request):
    main = get_renderer('templates/template.pt').implementation()
    return dict(title = 'Stand-Bys', main = main,
                user=request.user) 

@view_config(name='updates.json', renderer='json')
def updates_view(self):
    return [
        random.randint(0,100),
        random.randint(0,100),
        random.randint(0,100),
        random.randint(0,100),
        888,
    ]

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
                user=request.user)

    
@view_config(route_name='coverage', renderer='templates/coverage.pt',
             permission = 'Member')
def coverage(request):
    main = get_renderer('templates/template.pt').implementation()
    return dict(title = 'Coverage Requests', main = main,
                user=request.user)
    
   

    
@view_config(route_name='adduser', renderer='templates/adduser.pt',
             permission = 'admin')
def adduser(request):
    main = get_renderer('templates/template.pt').implementation()
    headers = [column.name for column in Users.__table__.columns][:-5]

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
        newuser.privileges = request.params['privileges']
        newuser.trainingvalue = request.params['trainingvalue']
        newuser.administrativevalue = request.params['administrativevalue']
        newuser.operationalvalue = request.params['operationalvalue']
        DBSession.add(newuser)
        
            
    Options = DBSession.query(Privileges).all()
    privilegesOptions = [option.privilege for option in Options]
    Options = DBSession.query(TrainingLevel).all()
    trainingOptions = [option.traininglevel for option in Options]
    Options = DBSession.query(AdministrativeStatus).all()
    administrativeOptions = [option.status for option in Options]
    Options = DBSession.query(OperationalStatus).all()
    operationalOptions = [option.status for option in Options]
    
    return dict(title = 'Add User',
                main = main,
                headers = headers,
                privilegesOptions = privilegesOptions,
                trainingOptions = trainingOptions,
                administrativeOptions = administrativeOptions,
                operationalOptions = operationalOptions,
                user=request.user
                )

@view_config(route_name='edituser', renderer='templates/edituser.pt',
             permission = 'admin')
def edituser(request):
    main = get_renderer('templates/template.pt').implementation()
    if 'userselected' in request.params:
        userselected = request.params['userselected']
    else:
        userselected = ''
    
    if 'form.submitted' in request.params:
        userselected = request.params['userselected']
        edit_user  = DBSession.query(Users).filter_by(username=userselected).first()
        edit_user.username = request.params['username']
        edit_user.password = request.params['password']
        edit_user.firstname = request.params['firstname']
        edit_user.middlename = request.params['middlename']
        edit_user.lastname = request.params['lastname']
        edit_user.birthday = datetime.date(int(request.params['year']),int(request.params['month']),int(request.params['day']))
        edit_user.street = request.params['street']
        edit_user.city = request.params['city']
        edit_user.state = request.params['state']
        edit_user.zipcode = request.params['zipcode']
        edit_user.residence = request.params['residence']
        edit_user.roomnumber = request.params['roomnumber']
        edit_user.phonenumber = request.params['phonenumber']
        edit_user.email = request.params['email']
        edit_user.privileges = request.params['privileges']
        edit_user.trainingvalue = request.params['trainingvalue']
        edit_user.administrativevalue = request.params['administrativevalue']
        edit_user.operationalvalue = request.params['operationalvalue']
        DBSession.add(edit_user)
        
    if 'form.selected' in request.params:
        userselected = request.params['selecteduser']
        edit_user  = DBSession.query(Users).filter_by(username=userselected).first()
    else:
        userselected = ''
        edit_user = Users('','','','','','','','','','','','','','','','','','','')

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
    
    return dict(title = 'Edit User',
                main = main,
                userselected = userselected,
                edit_user=edit_user,
                users = allusernames,
                privilegesOptions = privilegesOptions,
                trainingOptions = trainingOptions,
                administrativeOptions = administrativeOptions,
                operationalOptions = operationalOptions,
                user=request.user,
                )

@view_config(route_name='deleteuser', renderer='templates/deleteuser.pt',
             permission = 'admin')
def deleteuser(request):
    main = get_renderer('templates/template.pt').implementation()
    message = ''
    
    if 'form.submitted' in request.params:
            user_selected = request.params['delete_user']
            delete_user = DBSession.query(Users).filter_by(username=user_selected).first()
            if delete_user:
                name = delete_user.username
                DBSession.delete(delete_user)
                message = "{} has been deleted".format(name)
            else:
                message = "Please select a vaild username"

    allusers = DBSession.query(Users).order_by(Users.username).all() 
    allusernames = ["None"]+[auser.username for auser in allusers]

    return dict(title='Delete User', 
                main=main,
                allusernames=allusernames,
                message=message,
                user=request.user)
    

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
                user=request.user)

@view_config(route_name='addeditlinks', renderer='templates/addeditlinks.pt',
             permission = 'admin')
def addeditlinks(request):
    main = get_renderer('templates/template.pt').implementation()
    return dict(title = 'Add/Edit Links', main = main,
                user=request.user)

@view_config(route_name='addeditdocuments', renderer='templates/addeditdocuments.pt',
             permission = 'admin')
def addeditdocuments(request):
    main = get_renderer('templates/template.pt').implementation()
    return dict(title = 'Add/Edit documents', main = main,
                user=request.user)

@view_config(route_name='addeditminutes', renderer='templates/addeditminutes.pt',
             permission = 'admin')
def editmeetingminutes(request):
    main = get_renderer('templates/template.pt').implementation()
    return dict(title = 'Add/Edit Meeting Minutes', main = main,
                user=request.user)

@view_config(route_name='addeditpictures', renderer='templates/addeditpictures.pt',
             permission = 'admin')
def addeditpictures(request):
    main = get_renderer('templates/template.pt').implementation()
    return dict(title = 'Add/Edit Pictures', main = main,
                user=request.user)




@view_config(route_name='editportablenumbers', renderer='templates/editportablenumbers.pt',
             permission = 'admin')
def editportablenumbers(request):
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
    
    return dict(title = 'Edit Portable Numbers', 
                main = main,
                allusernames = allusernames,
                user=request.user)

@view_config(route_name='addeditcertifications', renderer='templates/addeditcertifications.pt',
             permission = 'admin')
def addeditcertifications(request):
    main = get_renderer('templates/template.pt').implementation()
    return dict(title = 'Add/Edit Certifications', main = main,
                user=request.user)
    
@view_config(route_name='addeditstandby', renderer='templates/addeditstandby.pt',
             permission = 'admin')
def addeditstandby(request):
    main = get_renderer('templates/template.pt').implementation()
    return dict(title = 'Add/Edit Standby', main = main,
                user=request.user)

@view_config(route_name='editdutycrew', renderer='templates/editdutycrew.pt',
             permission = 'admin')
def editdutycrew(request):
    main = get_renderer('templates/template.pt').implementation()
     
    return dict(title = 'Edit Duty Crew', 
                main = main,
                user=request.user)

@view_config(route_name='addeditannouncements', renderer='templates/addeditannouncements.pt',
             permission = 'admin')
def addeditannouncements(request):
    main = get_renderer('templates/template.pt').implementation()
    announcementchosen = ''
    form = ''
    
    if 'form.submitted' in request.params:
        if request.params['option'] == 'New':
            announcement = Announcements('','','','','','')
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
            announcement = Announcements('','','','','')
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
        announcement = Announcements('','','','','')
        announcementchosen = ''
    
    allannouncements = DBSession.query(Announcements).all() 
    announcements = [announcement.header for announcement in allannouncements]
    
    return dict(title='Add/Edit Announcements',
                main=main,
                announcements=announcements,
                announcement=announcement,
                form=form,
                announcementchosen=announcementchosen,
                user=request.user
                )



@view_config(route_name='addeditevents', renderer='templates/addeditevents.pt',
             permission='admin')
def addeditevents(request):
    main = get_renderer('templates/template.pt').implementation()

    return dict(
            title='Add/Edit Events', 
            main=main,
            user=request.user
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
        main = main,
        title = 'Login',
        message = message,
        url = request.application_url + '/login',
        came_from = came_from,
        login = login,
        password = password,
        user=request.user)

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

