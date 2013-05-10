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
    """This function returns a Pyramid WSGI application."""
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    authn_policy = AuthTktAuthenticationPolicy('sosecret', callback=groupfinder)
    authz_policy = ACLAuthorizationPolicy()

    
    config = Configurator(settings=settings,
                          root_factory='rescueweb.models.RootFactory')

    #config.include('pyramid_mailer')

    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_static_view('documents', 'documents', cache_max_age=3600)
    config.add_static_view('pictures', 'static/pictures', cache_max_age=3600)

    config.add_route('home', '/')
    config.add_route('history','/history')
    config.add_route('personnel','/personnel')
    config.add_route('announcements' , '/announcements')
    # Routes for events. These are events Campus Rescue Squad members can sign
    # up for.
    config.add_route('events' , '/events')
    config.add_route('event' , '/event/{eventid}')
    config.add_route('pictures' , '/pictures')
    config.add_route('join' , '/join')
    config.add_route('contact' , '/contact')
    config.add_route('links' , '/links')
    config.add_route('documents' , '/documents')
    config.add_route('minutes' , '/minutes')
    config.add_route('member_info' , '/member_info')

    # Routes for standbys. These are events Campus Rescue Squad members can sign
    # up for.
    config.add_route('standbys' , '/standbys')
    config.add_route('standby' , '/standby/{standbyid}')
    config.add_route('duty_crew_calendar', '/duty_crew_calendar')
    config.add_route('coverage' , '/coverage')
    
    # Routes for admin tools
    config.add_route('add_user' , '/add_user')
    config.add_route('edit_user' , '/edit_user')
    config.add_route('delete_user' , '/delete_user')
    config.add_route('edit_pages' , '/edit_pages')
    config.add_route('add_edit_links' , '/add_edit_links')
    config.add_route('add_edit_documents' , '/add_edit_documents')
    config.add_route('add_edit_minutes' , '/add_edit_minutes')
    config.add_route('add_edit_pictures' , '/add_edit_pictures')
    config.add_route('edit_portable_numbers' , '/edit_portable_numbers')
    config.add_route('set_duty_crew' , '/set_duty_crew')
    config.add_route('add_edit_certifications' , '/add_edit_certifications')
    config.add_route('add_edit_standby' , '/add_edit_standby')
    config.add_route('edit_duty_crew' , '/edit_duty_crew')
    config.add_route('add_edit_announcements' , '/add_edit_announcements')
    config.add_route('add_edit_events' , '/add_edit_events')
    config.add_route('email' , '/email')

    # Attach a `user' attribute to the request object that's passed around
    # everywhere. This user object only has `username' and `privileges'
    # attributes currently.
    config.add_request_method(get_user, 'user', reify=True)

    config.add_route('login', '/login')
    config.add_route('logout', '/logout')


    config.scan()
    return config.make_wsgi_app()
