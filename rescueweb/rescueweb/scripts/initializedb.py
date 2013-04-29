import os
import sys
import transaction
import datetime

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings, 
    setup_logging, 
    )

from ..models import (
    DBSession, 
    Users, 
    Events, 
    Certifications, 
    OperationalStatus, 
    AdministrativeStatus, 
    EboardPositions, 
    TrainingLevel, 
    Privileges, 
    Page, 
    Announcements, 
    Documents, 
    WebLinks, 
    Base, 
    StandBy,
	Pictures,
    )

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)

def main(argv = sys.argv):
    if len(argv) !=  2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind = engine)
    Base.metadata.create_all(engine)

    with transaction.manager:
        DBSession.add_all(
                [
                    Documents(name='Constitution', fileName='Constitution.pdf'),
                    Documents(name='Advancement Form', fileName='Advancement_Form.pdf'),
                    Documents(name='By-Laws', fileName='By-Laws.pdf'),
                    Documents(name='Standard Operating Guidelines', fileName='SOG.pdf'),
                ])

        DBSession.add_all(
                [
                    WebLinks(name='Potsdam Rescue', address='http://www.pvrs.org/'),
                    WebLinks(name='NYS Department of Health', address='http://www.health.state.ny.us/'),
                    WebLinks(name='FEMA Training Website', address='http://training.fema.gov/'),
                    WebLinks(name='North Country EMS', address='http://www.canton.edu/NCEMS'),
                    WebLinks(name='ICS Courses', address='http://hamradio.arc.nasa.gov/ICScourses.html'),
                ])
                    
        DBSession.add_all(
                [
                    Announcements(
                        header='Remember Paperwork', 
                        text='Please remember to submit all paperwork', 
                        priority=1, 
                        username='turdona193', 
                        posted=datetime.datetime.today()
                        ),

                    Announcements(
                        header='Crew Chief Signup', 
                        text='Please remember to sign up on the Crew Chief Calendar', 
                        priority=1, 
                        username='turdona193', 
                        posted=datetime.datetime.today()
                        ),

                    Announcements(header='Mixer', 
                        text='Hey Guys, There is a mixer happening Wednesday, Bring friends.', 
                        priority=1, 
                        username='turdona193', 
                        posted=datetime.datetime.today()
                        ),
                ])

        DBSession.add_all(
                [
                    Users(
                        username='turdona193', 
                        password='nick', 
                        firstname='Nicholas', 
                        middlename='Anthony', 
                        lastname='Turdo', 
                        birthday=datetime.date(1991, 1, 26), 
                        street = '3510 Barrington Dr', 
                        city='Potsdam', 
                        state='NY', 
                        zipcode='13676', 
                        residence='Townhouse', 
                        roomnumber='A1-104', 
                        phonenumber = 6462595690, 
                        email='turdona193@potsdam.edu', 
                        privileges=2, 
                        trainingvalue=3, 
                        administrativevalue=3, 
                        operationalvalue=4, 
                        portablenumber=10
                        ),

                    Users(
                        username='muehlbjp193', 
                        password='jared', 
                        firstname='Jared', 
                        middlename='Paul', 
                        lastname='Muehlbauer', 
                        birthday=datetime.date(1991, 12, 26), 
                        street = '2512 Barrington Dr', 
                        city='Potsdam', 
                        state='NY', 
                        zipcode='13676', 
                        residence='Townhouse', 
                        roomnumber='A1-201', 
                        phonenumber = 6462595690, 
                        email='muehlbjp193@potsdam.edu', 
                        privileges=2, 
                        trainingvalue=3, 
                        administrativevalue=4, 
                        operationalvalue=6, 
                        portablenumber=7
                        ),

                    Users(
                        username='guarintb193', 
                        password='tim', 
                        firstname='Tim', 
                        middlename='Bret', 
                        lastname='Guarino', 
                        birthday=datetime.date(1991, 10, 31), 
                        street = '1459 Barrington Dr', 
                        city='Potsdam', 
                        state='NY', 
                        zipcode='13676', 
                        residence='Townhouse', 
                        roomnumber='A1-204', 
                        phonenumber = 6462595690, 
                        email='guarintb193@potsdam.edu', 
                        privileges=2, 
                        trainingvalue=3, 
                        administrativevalue=4, 
                        operationalvalue=6, 
                        portablenumber=1
                        ),
                ])
        
        DBSession.add_all(
                [
                    Certifications(
                        username='turdona193', 
                        certification='CPR', 
                        certnumber=None, 
                        expiration='02/2015'
                        ),

                    Certifications(
                        username='turdona193',
                        certification='EMT-Basic',
                        certnumber=389992,
                        expiration='06/2014'
                        ),

                    Certifications(
                        username='muehlbjp193',
                        certification='CPR',
                        certnumber=None,
                        expiration='05/2014'
                        ),

                    Certifications(
                        username='muehlbjp193',
                        certification='EMT-Basic',
                        certnumber=380246,
                        expiration='06/2013'
                        ),

                    Certifications(
                        username='guarintb193',
                        certification='CPR',
                        certnumber=None,
                        expiration='10/2014'
                        ),

                    Certifications(
                        username='guarintb193',
                        certification='EMT-Basic',
                        certnumber=384850,
                        expiration='01/2014'
                        ),
                ])
        
        DBSession.add_all(
                [
                    OperationalStatus(operationalvalue=0, status='Inactive'),
                    OperationalStatus(operationalvalue=1, status='Probationary'),
                    OperationalStatus(operationalvalue=2, status='Observational'),
                    OperationalStatus(operationalvalue=3, status='Active'),
                    OperationalStatus(operationalvalue=4, status='Active-EMT'),
                    OperationalStatus(operationalvalue=5, status='ProbationaryCrewChief'),
                    OperationalStatus(operationalvalue=6, status='CrewChief'),
                    OperationalStatus(operationalvalue=7, status='MedicalDirector'),
                ])

        DBSession.add_all(
                [
                    AdministrativeStatus(administrativevalue=0, status='Inactive'),
                    AdministrativeStatus(administrativevalue=1, status='Probationary'),
                    AdministrativeStatus(administrativevalue=2, status='Observational'),
                    AdministrativeStatus(administrativevalue=3, status='Active'),
                    AdministrativeStatus(administrativevalue=4, status='EBoard'),
                    AdministrativeStatus(administrativevalue=5, status='HonorRoll'),
                    AdministrativeStatus(administrativevalue=6, status='Advisor'),
                    AdministrativeStatus(administrativevalue=7, status='MedicalDirector'),
                ])

        DBSession.add_all(
                [
                    EboardPositions(position='Chief', username='guarintb193'),
                    EboardPositions(position='Parliamentarian', username='muehlbjp193'),
                ])
        
        DBSession.add_all(
                [
                    TrainingLevel(trainingvalue=0, traininglevel='none'),
                    TrainingLevel(trainingvalue=1, traininglevel='CPR'),
                    TrainingLevel(trainingvalue=2, traininglevel='EMT-Student'),
                    TrainingLevel(trainingvalue=3, traininglevel='EMT-Basic'),
                    TrainingLevel(trainingvalue=4, traininglevel='AEMT-Critical Care'),
                    TrainingLevel(trainingvalue=5, traininglevel='AEMT-Paramedic'),
                ])
        
        DBSession.add_all(
                [
                    Privileges(
                        privilegevalue=0, 
                        privilege='Guest', 
                        pyramidsecuritygroup='guest'
                        ),

                    Privileges(
                        privilegevalue=1, 
                        privilege='Member', 
                        pyramidsecuritygroup='member'
                        ),

                    Privileges(
                        privilegevalue=2, 
                        privilege='Admin', 
                        pyramidsecuritygroup='admin'
                    ),
                ])

        DBSession.add_all(
                [
                    Events(
                        startdatetime=datetime.datetime(2000, 1, 1),
                        enddatetime=datetime.datetime(2000, 1, 3),
                        name='Party',
                        notes='nothing',
                        privileges=0
                        ),

                    Events(
                        startdatetime=datetime.datetime(2001, 2, 3),
                        enddatetime=datetime.datetime(2001, 10, 15),
                        name='Dance',
                        notes='not going',
                        privileges=0
                        ),

                    Events(
                        startdatetime=datetime.datetime(2002, 5, 5),
                        enddatetime=datetime.datetime(2002, 5, 8),
                        name='Grad',
                        notes='we leave!',
                        privileges=0
                        )
                ])

        DBSession.add_all(
                [
                    StandBy(
                        event='5K run',
                        location='Maxci Field House',
                        notes='''This is a very important standby! A lot of people
                        are bound to get hurt!''',
                        startdatetime=datetime.datetime(2013, 4, 15),
                        enddatetime=datetime.datetime(2013, 4, 15)
                        ),

                    StandBy(
                        event='Relay for Life',
                        location='Stillman Hall',
                        notes='''Another event where an ambulance is surely
                        needed!''',
                        startdatetime=datetime.datetime(2013, 4, 20),
                        enddatetime=datetime.datetime(2013, 4, 20)
                        ),

                    StandBy(
                        event='Bake Sale',
                        location='Townhouse J4',
                        notes='''Would you really trust a Bake Sale at Townhouse
                        J4?''',
                        startdatetime=datetime.datetime(2013, 4, 1),
                        enddatetime=datetime.datetime(2013, 4, 1)
                        ),

                    StandBy(
                        event='Cookies for Sale',
                        location='Barrington Union',
                        notes='''The REAL Bake sale.''',
                        startdatetime=datetime.datetime(2013, 4, 1),
                        enddatetime=datetime.datetime(2013, 4, 1)
                        ),
                ])

        DBSession.add_all(
                [
                    Page(name='Home', data=("""Welcome to the SUNY Potsdam
                    Campus Rescue Squad website! </br> Currently the CRS staff
                    consists of approximately 22 members, many of which have
                    completed the NYS EMT Curriculum. Also, many of the members
                    are currently enrolled in the EMT basic class. </br> If you
                    wish to report a medical emergency please call x2222 and ask
                    for CRS assistance and be ready to give the following
                    information: a reason for calling (the medical emergency),
                    your name, the location of the medical emergency, and
                    remember to remain calm.</br> Disclaimer: Campus Rescue
                    Squad takes privacy very seriously. Any images shown on this
                    site are taken from mock events and do not show actual
                    patients.""")),
        
                    Page(name='History', data="""The SUNY Potsdam Campus Rescue
                    Squad started in 1992 as a group of college students that
                    formed together to provide much needed medical coverage for
                    SUNY Potsdam varsity athletic events as well as various
                    other college events. </br> As responsibilities as a
                    certified agency came, so did the necessity for
                    communications. Through their menial budget CRS was able to
                    purchase four radios. Along with those radios was a donation
                    of 12 pagers, which finally allowed Campus Safety (now
                    University Police) to activate CRS via pager alert. </br>

                    Almost 17 years later, Campus Rescue continues the tradition of quality
                    emergency medical care 24/7 while school is in session. Because of the
                    dedication of true professional EMS providers, Campus Rescue continues to thrive
                    as an important link in prehospital care in SUNY Potsdam. </br>

                    The Squad today (as of 2008) has approximately 25 members, 14 of which are NYS
                    certified EMT's, 6 of which are currently enrolled in the NYS EMT-B curriculum,
                    and 23 of which are American Heart Association BCLS certified in AED and
                    CPR.</br>

                    The Squad currently has 7 NYS DOH Part 800 compliant BLS jump bags. One bag is
                    housed in University Police dispatch, one at the Crumb Library, and 2 are housed
                    in the squad equipment room. CRS is approved through medical direction and NY to
                    administer albuterol for respiratory emergencies and Epinephrine for
                    anaphylaxis. The squad also owns an AED, housed in one of University Police's
                    patrol cars. AEDs are also housed in every building on campus due to the PAD
                    program.</br>

                    Campus Rescue runs on average approximately 150 calls and standbys each
                    year."""),
        
                    Page(name='Join', data=("""The Campus Rescue Squad at SUNY
                    Potsdam is always open for new members! If you are
                    interested in joining the squad, email rescue@potsdam.edu
                    </br> The official CRS application is located here. General
                    membership meetings are held bi-weekly in Forum Room 204 at
                    8:00pm, preceded by a training at 7:00pm in the Union's Fire
                    Side Lounge. The meeting dates for the Spring 2012 semester
                    are: To be Announced! </br> 
                    
                    CRS does not discriminate
                    membership because of race, religion, creed, color, or
                    lifestyle preference.""")
                    ),
        
                    Page(name='ContactUs', data=""" On Campus Emergency:
                    315-267-2222 </br>
                    Off Campus Emergency: 911 </br>
                    Business Line: 315-267-2253 </br>
                    Mailing Address: 9010 Barrington Drive, Potsdam, NY 13676</br>
                    Office Location: Sission Basement </br>
                    """
                    ),
                ])
        DBSession.add_all(
                [
                    Pictures(picture='/pictures/eqptip.jpg',description="This is a picture of our equipment."),
                    Pictures(picture='/pictures/mock1.jpg',description="Pictures from our 2004 Mock DWI event."),
                ])
