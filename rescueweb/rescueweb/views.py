from pyramid.response import Response
from pyramid.view import view_config
from pyramid.renderers import get_renderer

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
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
    return dict(title='Home', main=main)

@view_config(route_name='history', renderer='templates/history.pt')
def history(request):
    main = get_renderer('templates/template.pt').implementation()
    return dict(title = 'History', main = main)

@view_config(route_name='personnel', renderer='templates/personnel.pt')
def personal(request):
    main = get_renderer('templates/template.pt').implementation()
    personal = DBSession.query(users).all()
    
       # headers = [column.name for column in personal[0].__table__.columns]
    return dict(title = 'Personal', main = main)

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

