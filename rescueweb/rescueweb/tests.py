import unittest
import transaction

from pyramid import testing

def _initTestingDB():
    from sqlalchemy import create_engine
    from rescueweb.models import (
        DBSession,
        Page,
        Base
        )
    engine = create_engine('sqlite://')
    Base.metadata.create_all(engine)
    DBSession.configure(bind=engine)
    with transaction.manager:
        model = Page('FrontPage', 'This is the front page')
        DBSession.add(model)
    return DBSession

class ViewPageTests(unittest.TestCase):
    def setUp(self):
        self.session = _initTestingDB()
        self.config = testing.setUp()

    def tearDown(self):
        self.session.remove()
        testing.tearDown()

    def _callFUT(self, request):
        from tutorial.views import view_page
        return view_page(request)

    def test_it(self):
        from tutorial.models import Page
        request = DBSession.DummyRequest()
        request.matchdict['history'] = 'DoIExist?'
        page = Page('DoIExist?', 'blah blah something')
        self.registerRoutes(self.config)
        info = self._callFUT(request)
        self.assertEqual(info['page'], page)
        self.assertEqual('testing', 'failure')

class FunctionalTests(unittest.TestCase):
    def setUp(self):
        from rescueweb import main
        settings = { 'sqlalchemy.url': 'sqlite://' }
        app = main({}, **settings)
        from webtest import TestApp
        self.testapp = TestApp(app)

    def test_it(self):
        #pages = [
        #        '/', '/history', '/personnel', '/announcements', '/events',
        #        '/pictures', '/join', '/contact', '/links', '/documents',
        #        '/minutes', '/member_info', '/standbys', '/duty_crew_calendar',
        #        '/coverage', '/add_user', '/edit_user', '/delete_user',
        #        '/edit_pages', '/add_edit_links', '/add_edit_documents',
        #        '/add_edit_minutes', '/add_edit_pictures',
        #        '/edit_portable_numbers', '/add_edit_certifications',
        #        '/add_edit_standby', '/edit_duty_crew',
        #        '/add_edit_announcements', '/add_edit_events'
        #        ]
        pages = ['/']
        content = ['Welcome to the SUNY Potsdam Campus Rescue Squad website!']

        for page, title in zip(pages, content):
            res = self.testapp.get(page, status=200)
            self.assertIn(bytes(title, 'utf-8'), res.body)
