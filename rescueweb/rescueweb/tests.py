import unittest
import transaction

from pyramid import testing

from .models import DBSession


class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        #from sqlalchemy import create_engine
        #engine = create_engine('sqlite://')
        #from .models import (
        #    Base,
        #    MyModel,
        #    )
        #DBSession.configure(bind=engine)
        #Base.metadata.create_all(engine)
        #
        #with transaction.manager:
        #    model = MyModel(name='one', value=55)
        #    DBSession.add(model)

    def tearDown(self):
        #DBSession.remove()
        testing.tearDown()

    def test_it(self):
        #from .views import my_view
        #request = testing.DummyRequest()
        #info = my_view(request)
        #self.assertEqual(info['one'].name, 'one')
        #self.assertEqual(info['project'], 'rescueweb')
        pass

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
