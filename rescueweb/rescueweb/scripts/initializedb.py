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
    users,
    events,
    emtcert,
    certifications,
    operationalstatus,
    administrativestatus,
    eboardpositions,
    traininglevel,
    privileges,
    Page,
    Announcements,
    Documents,
    weblinks,
    Base,
    )


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        model = Page(name = 'Home', data = ("""Welcome to the SUNY Potsdam Campus Rescue Squad website! </br>
Currently the CRS staff consists of approximately 22 members, many of which have completed the NYS EMT Curriculum. Also, many of the members are currently enrolled in the EMT basic class. </br>
If you wish to report a medical emergency please call x2222 and ask for CRS assistance and be ready to give the following information: a reason for calling (the medical emergency), your name, the location of the medical emergency, and remember to remain calm.</br>
Disclaimer: Campus Rescue Squad takes privacy very seriously. Any images shown on this site are taken from mock events and do not show actual patients."""))
        DBSession.add(model)
        
        model = Page(name = 'History', data = """The SUNY Potsdam Campus Rescue Squad started in 1992 as a group of college students that formed together to provide much needed medical coverage for SUNY Potsdam varsity athletic events as well as various other college events. </br>
As responsibilities as a certified agency came, so did the necessity for communications. Through their menial budget CRS was able to purchase four radios. Along with those radios was a donation of 12 pagers, which finally allowed Campus Safety (now University Police) to activate CRS via pager alert. </br>

Almost 17 years later, Campus Rescue continues the tradition of quality emergency medical care 24/7 while school is in session. Because of the dedication of true professional EMS providers, Campus Rescue continues to thrive as an important link in prehospital care in SUNY Potsdam. </br>

The Squad today (as of 2008) has approximately 25 members, 14 of which are NYS certified EMT's, 6 of which are currently enrolled in the NYS EMT-B curriculum, and 23 of which are American Heart Association BCLS certified in AED and CPR.</br>

The Squad currently has 7 NYS DOH Part 800 compliant BLS jump bags. One bag is housed in University Police dispatch, one at the Crumb Library, and 2 are housed in the squad equipment room. CRS is approved through medical direction and NY to administer albuterol for respiratory emergencies and Epinephrine for anaphylaxis. The squad also owns an AED, housed in one of University Police's patrol cars. AEDs are also housed in every building on campus due to the PAD program.</br>

Campus Rescue runs on average approximately 150 calls and standbys each year.""")
        DBSession.add(model)
        
        
        
        model = Page(name = 'Join', data = ("""The Campus Rescue Squad at SUNY Potsdam is always open for new members! If you are interested in joining the squad, email rescue@potsdam.edu </br>
                                            The official CRS application is located here. General membership meetings are held bi-weekly in Forum Room 204 at 8:00pm, preceded by a training at 7:00pm in the Union's Fire Side Lounge. The meeting dates for the Spring 2012 semester are: To be Announced! </br>
                                            CRS does not discriminate membership because of race, religion, creed, color, or lifestyle preference."""))
        DBSession.add(model)
        
        model = Page(name = 'ContactUs', data = """ On Campus Emergency: 315-267-2222 </br>
        Off Campus Emergency: 911 </br>
        Business Line: 315-267-2253 </br>
        Mailing Address: 9010 Barrington Drive, Potsdam, NY 13676</br>
        Office Location: Sission Basement </br>
        
        """)
        DBSession.add(model)

        
        model = Documents(name = 'Constitution', fileName = 'Constitution.pdf')
        DBSession.add(model)
        model = Documents(name = 'Advancement Form', fileName = 'Advancement_Form.pdf')
        DBSession.add(model)
        model = Documents(name = 'By-Laws', fileName = 'By-Laws.pdf')
        DBSession.add(model)
        model = Documents(name = 'Standard Operating Guidelines', fileName = 'SOG.pdf')
        DBSession.add(model)
        
        model = weblinks(name = 'Potsdam Rescue' , address = 'http://www.pvrs.org/')
        DBSession.add(model)
        model = weblinks(name = 'NYS Department of Health' , address = 'http://www.health.state.ny.us/')
        DBSession.add(model)
        model = weblinks(name = 'FEMA Training Website' , address = 'http://training.fema.gov/')
        DBSession.add(model)
        model = weblinks(name = 'North Country EMS' , address = 'http://www.canton.edu/NCEMS')
        DBSession.add(model)
        model = weblinks(name = 'ICS Courses' , address = 'http://hamradio.arc.nasa.gov/ICScourses.html')
        DBSession.add(model)
        
        
        model = Announcements(header = 'Remember Paperwork', text = 'Please remember to submit all paperwork', priority = 1, username = 'turdona193' , posted = datetime.datetime.today())
        DBSession.add(model)
        model = Announcements(header = 'Crew Chief Signup', text = 'Please remember to sign up on the Crew Chief Calendar', priority = 1, username = 'turdona193', posted = datetime.datetime.today())
        DBSession.add(model)
        model = Announcements(header = 'Mixer', text = 'Hey Guys, There is a mixer happening Wednesday, Bring friends.', priority = 1, username = 'turdona193', posted = datetime.datetime.today())
        DBSession.add(model)

        
        
        user = users(username = 'turdona193', password = 'nick',firstname = 'Nicholas',middlename = 'Anthony',lastname = 'Turdo',birthday = datetime.date(1991,1,26),
                     street = '3510 Barrington Dr',city = 'Potsdam', state = 'NY',zipcode = '13676',residence = 'Townhouse',roomnumber = 'A1-104',
                     phonenumber = 6462595690,email = 'turdona193@potsdam.edu',privileges = 2,trainingvalue = 3,administrativevalue = 3,operationalvalue = 4, portablenumber = 10)
        DBSession.add(user)
        user = users(username = 'muehlbjp193', password = 'jared',firstname = 'Jared',middlename = 'Paul',lastname = 'Muehlbauer',birthday = datetime.date(1991,12,26),
                     street = '2512 Barrington Dr',city = 'Potsdam', state = 'NY',zipcode = '13676',residence = 'Townhouse',roomnumber = 'A1-201',
                     phonenumber = 6462595690,email = 'muehlbjp193@potsdam.edu',privileges = 2,trainingvalue = 3,administrativevalue = 4,operationalvalue = 6, portablenumber = 7)
        DBSession.add(user)
        user = users(username = 'guarintb193', password = 'tim',firstname = 'Tim',middlename = 'Bret',lastname = 'Guarino',birthday = datetime.date(1991,10,31),
                     street = '1459 Barrington Dr',city = 'Potsdam', state = 'NY',zipcode = '13676',residence = 'Townhouse',roomnumber = 'A1-204',
                     phonenumber = 6462595690,email = 'guarintb193@potsdam.edu',privileges = 2,trainingvalue = 3,administrativevalue = 4,operationalvalue = 6, portablenumber = 1)
        DBSession.add(user)
        
        cert = emtcert(username = 'turdona193',certnumber = 389992)
        DBSession.add(cert)
        cert = emtcert(username = 'muehlbjp193',certnumber = 380246)
        DBSession.add(cert)
        cert = emtcert(username = 'guarintb193',certnumber = 384850)
        DBSession.add(cert)        
        
        cert = certifications(username = 'turdona193',certification = 'CPR',expiration = '02/2015')
        DBSession.add(cert)
        cert = certifications(username = 'turdona193',certification = 'EMT-Basic',expiration = '06/2014')
        DBSession.add(cert)
        cert = certifications(username = 'muehlbjp193',certification = 'CPR',expiration = '05/2014')
        DBSession.add(cert)
        cert = certifications(username = 'muehlbjp193',certification = 'EMT-Basic',expiration = '06/2013')
        DBSession.add(cert)
        cert = certifications(username = 'guarintb193',certification = 'CPR',expiration = '10/2014')
        DBSession.add(cert)        
        cert = certifications(username = 'guarintb193',certification = 'EMT-Basic',expiration = '01/2014')
        DBSession.add(cert)        
        
        status = operationalstatus(operationalvalue = 0,status = 'Inactive')
        DBSession.add(status)
        status = operationalstatus(operationalvalue = 1,status = 'Probationary')
        DBSession.add(status)
        status = operationalstatus(operationalvalue = 2,status = 'Observational')
        DBSession.add(status)
        status = operationalstatus(operationalvalue = 3,status = 'Active')
        DBSession.add(status)
        status = operationalstatus(operationalvalue = 4,status = 'Active-EMT')
        DBSession.add(status)
        status = operationalstatus(operationalvalue = 5,status = 'ProbationaryCrewChief')
        DBSession.add(status)
        status = operationalstatus(operationalvalue = 6,status = 'CrewChief')
        DBSession.add(status)
        status = operationalstatus(operationalvalue = 7,status = 'MedicalDirector')
        DBSession.add(status)
      
        status = administrativestatus(administrativevalue = 0,status = 'Inactive')
        DBSession.add(status)
        status = administrativestatus(administrativevalue = 1,status = 'Probationary')
        DBSession.add(status)
        status = administrativestatus(administrativevalue = 2,status = 'Observational')
        DBSession.add(status)
        status = administrativestatus(administrativevalue = 3,status = 'Active')
        DBSession.add(status)
        status = administrativestatus(administrativevalue = 4,status = 'EBoard')
        DBSession.add(status)
        status = administrativestatus(administrativevalue = 5,status = 'HonorRoll')
        DBSession.add(status)
        status = administrativestatus(administrativevalue = 6,status = 'Advisor')
        DBSession.add(status)
        status = administrativestatus(administrativevalue = 7,status = 'MedicalDirector')
        DBSession.add(status)

        
        position = eboardpositions(position = 'Chief',username = 'guarintb193')
        DBSession.add(position)
        position = eboardpositions(position = 'Parliamentarian',username = 'muehlbjp193')
        DBSession.add(position)
        
        training = traininglevel(trainingvalue = 0,traininglevel = 'none')
        DBSession.add(training)
        training = traininglevel(trainingvalue = 1,traininglevel = 'CPR')
        DBSession.add(training)
        training = traininglevel(trainingvalue = 2,traininglevel = 'EMT-Student')
        DBSession.add(training)
        training = traininglevel(trainingvalue = 3,traininglevel = 'EMT-Basic')
        DBSession.add(training)
        training = traininglevel(trainingvalue = 4,traininglevel = 'AEMT-Critical Care')
        DBSession.add(training)
        training = traininglevel(trainingvalue = 5,traininglevel = 'AEMT-Paramedic')
        DBSession.add(training)
        
        privilege = privileges(privilegevalue=0,privilege='Guest')
        DBSession.add(privilege)
        privilege = privileges(privilegevalue=1,privilege='Member')
        DBSession.add(privilege)
        privilege = privileges(privilegevalue=2,privilege='Admin')
        DBSession.add(privilege)

        event = events(eventid=1, startdatetime=datetime.datetime(2000, 1, 1), enddatetime=datetime.datetime(2000, 1, 3), name='Party', notes='nothing', privileges=0)
        DBSession.add(event);
        event = events(eventid=2, startdatetime=datetime.datetime(2001, 2, 3), enddatetime=datetime.datetime(2001, 10, 15), name='Dance', notes='not going', privileges=0)
        DBSession.add(event);
        event = events(eventid=3, startdatetime=datetime.datetime(2002, 5, 5), enddatetime=datetime.datetime(2002, 5, 8), name='Grad', notes='we leave!', privileges=0)
        DBSession.add(event);
