from pyramid.response import Response
from pyramid.view import view_config
from pyramid.renderers import get_renderer

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    Page,
    users,
    emtcert,
    certifications,
    operationalstatus,
    administrativestatus,
    eboardpositions,
    traininglevel,
    )

@view_config(route_name='home', renderer='templates/home.pt')
def home(request):
    main = get_renderer('templates/template.pt').implementation()
    page = DBSession.query(Page).filter_by(name='Home').first()

    return dict(title='Home', main=main , page = page)

@view_config(route_name='history', renderer='templates/history.pt')
def history(request):
    main = get_renderer('templates/template.pt').implementation()
    page = DBSession.query(Page).filter_by(name='History').first()
    return dict(title = 'History', main = main , page = page)

@view_config(route_name='personnel', renderer='templates/personnel.pt')
def personal(request):
    main = get_renderer('templates/template.pt').implementation()
    page = DBSession.query(users).all()
    
    headers = [column.name for column in page[0].__table__.columns]
    return dict(title = 'Personnel', main = main, personnel = page, headers = headers)

@view_config(route_name='duty_crew_calendar', renderer='templates/duty_crew_calendar.pt')
def duty_crew_calendar(request):
    main = get_renderer('templates/template.pt').implementation()
    return dict(title = 'Duty Crew Calendar', main = main)


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

