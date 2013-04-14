from pyramid.config import Configurator
from sqlalchemy import engine_from_config

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
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('history','/history')
    config.add_route('personnel','/personnel')
    config.add_route('duty_crew_calendar', '/duty_crew_calendar')
    config.add_route('announcements' , '/announcements')
    config.add_route('join' , '/join')
    
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')

    config.scan()
    return config.make_wsgi_app()
