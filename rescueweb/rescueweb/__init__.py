from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from rescueweb.security import groupfinder

from rescueweb.security import (
    groupfinder,
    get_user,
    )

from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    
    authn_policy = AuthTktAuthenticationPolicy('sosecret', callback=groupfinder)
    authz_policy = ACLAuthorizationPolicy()
    config = Configurator(settings=settings,
                          root_factory='rescueweb.models.RootFactory')
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_static_view('documents', 'documents', cache_max_age=3600)

    config.add_route('home', '/')
    config.add_route('history','/history')
    config.add_route('personnel','/personnel')

    config.add_route('announcements' , '/announcements')
    config.add_route('events' , '/events')
    config.add_route('pictures' , '/pictures')
    
    config.add_route('join' , '/join')
    config.add_route('contact' , '/contact')
    config.add_route('links' , '/links')

    config.add_route('documents' , '/documents')
    config.add_route('minutes' , '/minutes')
    config.add_route('memberinfo' , '/memberinfo')
    
    config.add_route('standbys' , '/standbys')
    config.add_route('duty_crew_calendar', '/duty_crew_calendar')
    config.add_route('coverage' , '/coverage')
    
    config.add_route('adduser' , '/adduser')
    config.add_route('edituser' , '/edituser')
    config.add_route('deleteuser' , '/deleteuser')
    
    config.add_route('editpages' , '/editpages')
    config.add_route('addeditlinks' , '/addeditlinks')
    config.add_route('addeditdocuments' , '/addeditdocuments')
    config.add_route('addeditminutes' , '/addeditminutes')
    config.add_route('addeditpictures' , '/addeditpictures')
    
    config.add_route('editportablenumbers' , '/editportablenumbers')
    config.add_route('addeditcertifications' , '/addeditcertifications')
    
    config.add_route('addeditstandby' , '/addeditstandby')
    config.add_route('editdutycrew' , '/editdutycrew')
    
    config.add_route('add_edit_announcements' , '/add_edit_announcements')
    config.add_route('addeditevents' , '/addeditevents')

    # Attach a `user' attribute to the request object that's passed around
    # everywhere. This user object only has `username' and `privileges'
    # attributes currently.
    config.add_request_method(get_user, 'user', reify=True)
    
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')


    
    config.scan()
    return config.make_wsgi_app()
