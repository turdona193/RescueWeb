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
    MeetingMinutes,
    Pictures,
    DutyCrews,
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
                    Documents(name='Constitution', filename='Constitution.pdf'),
                    Documents(name='Advancement Form', filename='Advancement_Form.pdf'),
                    Documents(name='By-Laws', filename='By-Laws.pdf'),
                    Documents(name='Standard Operating Guidelines', filename='SOG.pdf'),
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
                        phonenumber=6462595690, 
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
                    EboardPositions(eboardposition='Chief Line Officer', username='guarintb193', bio=''),
                    EboardPositions(eboardposition='Assistant Chief Line Officer', username='', bio=''),
                    EboardPositions(eboardposition='President', username='', bio=''),
                    EboardPositions(eboardposition='Vice President', username='', bio=''),
                    EboardPositions(eboardposition='Treasurer', username='', bio=''),
                    EboardPositions(eboardposition='Secretary', username='', bio=''),
                    EboardPositions(eboardposition='Parliamentarian', username='muehlbjp193', bio=''),
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
                        startdatetime=datetime.datetime(2013, 5, 15),
                        name='Birthday Party',
                        notes='Someone is having a birthday today!',
                        location = 'Townhouse J4',
                        privileges=0
                        ),

                    Events(
                        startdatetime=datetime.datetime(2013, 5, 15),
                        name='A Secret Gathering',
                        notes='Only Admins should be able to view this Event',
                        location = 'Area 51',
                        privileges=2
                        ),

                    Events(
                        startdatetime=datetime.datetime(2013, 5, 5),
                        name='Dance',
                        notes='not going',
                        location = 'Union MPR',
                        privileges=1
                        ),

                    Events(
                        startdatetime=datetime.datetime(2013, 5, 30),
                        name='Grad',
                        notes='we leave!',
                        location = 'Accademic Quad',
                        privileges=2
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
                        ),

                    StandBy(
                        event='Relay for Life',
                        location='Stillman Hall',
                        notes='''Another event where an ambulance is surely
                        needed!''',
                        startdatetime=datetime.datetime(2013, 4, 20),
                        ),

                    StandBy(
                        event='Bake Sale',
                        location='Townhouse J4',
                        notes='''Would you really trust a Bake Sale at Townhouse
                        J4?''',
                        startdatetime=datetime.datetime(2013, 4, 1),
                        ),

                    StandBy(
                        event='Cookies for Sale',
                        location='Barrington Union',
                        notes='''The REAL Bake sale.''',
                        startdatetime=datetime.datetime(2013, 4, 1),
                        ),
                ])

        DBSession.add_all(
                [
                    Page(name='Home', data=("""
Welcome to the State University of New York at Potsdam Campus Rescue Squad (CRS) website.<br/><br/>

The Campus Rescue Squad is a New York State First Response agency that responds to medical emergencies on SUNY Potsdam Campus.  Our agency provides high quality, professional medical care to all members and visitors to SUNY Potsdam.  We currently have 18 dedicated volunteers, 9 of whom are New York State certified Emergency Medical Technicians, and another 4 who are now taking the class.  <br/><br/>

In case of an Emergency on campus, please contact University Police at (315) 267-2222.  Dispatchers are present at all times to assist you and dispatch Police, Fire and Emergency Medical Services as necessary in case of an emergency.  Be prepared to provide your name as well as the nature and location of the emergency.<br/><br/>

CRS responded to over 200 medical emergencies, standbys and requests for assistance in 2012.  Our squad also provides medical training on campus; from CPR and First Aid classes to opportunities to take the EMT-Basic class through SUNY Canton.<br/><br/>

Please visit us in our office in Sisson Hall Room (#) or contact us to learn about ways you can help your campus community, upcoming classes, or to join our team of dedicated volunteers.  <br/><br/>

Campus Rescue Squad takes privacy very seriously.  Any and all patient information is confidential and will not be provided to anyone except for the patient and other medical services.  <br/><br/>
""")),
        
                    Page(name='History', data=("""Campus Rescue Squad was founded in 1992 as an organization to provide medical coverage for SUNY Potsdam athletic and large campus events.  By the next year, CRS was providing coverage for the majority of on campus events and continued to expand its medical coverage and resources.<br/><br/>  

In September 2004, reflecting the efforts and hard work of the many volunteers, Campus Rescue became a New York State Department of Health certified Emergency First Response Agency.  CRS became able to provide 24/7 first response care and sponsor members to take the EMT-Basic course, in addition to providing medical coverage for campus events.  With this came the ability to activate Campus Rescue Squad for medical emergencies through the use of radio and pager alerts.<br/><br/>  

Having just celebrated its 20th anniversary, as well as its 9th year in service as a First Response Agency, Campus Rescue continues to serve the SUNY Potsdam community.  Expanding on a great tradition of professional involvement, CRS remains an important link in pre-hospital care in Potsdam.  <br/><br/>

Our members are all certified in AED and CPR and a NYS EMT responds to every call or standby that Campus Rescue covers.  Most of our members are EMT certified and many are also members of other EMS agencies, both at home and in the North Country.  We work closely both with University Police and with Potsdam Volunteer Rescue Squad to ensure safety and response to emergency situations.<br/><br/>  

We have also expanded our resources to include 9 Basic Life Support jump bags, housed in different areas on campus for easy access and quick response.  CRS now has over 10 radios and a number of pagers to effectively communicate with University Police, Dispatch, and the broad range of St. Lawrence County EMS services.  AEDs are now also available in every academic building for public use<br/><br/>
""")),
        
                    Page(name='ContactUs', data="""
In case of on-campus emergency:  (315) 267-2222  <br/>
In case of off-campus emergency: 911  <br/>  <br/>

Email: rescue@potsdam.edu  <br/>
Business Phone: (315) 267-2253  <br/>
Mailing Address: 9010 Barrington Dr. Potsdam NY, 13676  <br/>
Office Location: Sisson Hall Room (#)  <br/>  <br/>

Timothy Guarino, EMT-B  <br/>
Chief Line Officer  <br/>
email:  <br/>  <br/>

Andrew DiFabbio, EMT-B  <br/>
Assistant Chief Line Officer  <br/>
email:  <br/>  <br/>

Tammy Zanker, EMT-B  <br/>
President   <br/>
email:  <br/>  <br/>

Anthony Arena  <br/>
Vice President  <br/>
email:  <br/>  <br/>

Bobby Berrios, EMT-B  <br/>
Treasurer  <br/>
email:  <br/>  <br/>

Jarrett Bond, EMT-B  <br/>
Secretary  <br/>
email:  <br/>  <br/>

Jared Muehlbauer, EMT-B  <br/>
Parliamentarian  <br/>
email: muehlbjp193@potsdam.edu  <br/>  <br/>
                    """
                    ),
                    Page(name='Join', data=("""
Campus Rescue Squad always welcomes anyone interested in becoming part of our volunteer team.  If  interested, please email us at rescue@potsdam.edu, stop by our office, or come to one of our weekly meetings, held in the Union Forum, Room 204, Sundays at 8:00 pm.    <br/>  <br/>

By joining, you will be a part of a close-knit, dedicated team of volunteers.  We provide medical training and experience to introduce you to the field of EMS and can sponsor members to take the Emergency Medical Technician class, free of charge.  Members gain a great deal of networking opportunities with other professional agencies and University Police as well as a great item for their resume.  Most importantly, however, joining us allows you to be part of an excellent service that contributes and gives back to the SUNY Potsdam community every day.  As a squad, CRS is first and foremost here to help at any time, even and especially when situations are at their worst.    <br/>  <br/>

Our application is located here.  Any and all members of the SUNY Potsdam community are welcome and able to join, regardless of previous experience, training or background.    <br/>  <br/>

Just as all of the SUNY Potsdam community, CRS does not discriminate membership because of race, religion, creed, color, or lifestyle preference.  <br/>
""")),
                ])
        DBSession.add_all(

                [MeetingMinutes(datetime = datetime.datetime(2013,4,28),
                                header = 'Officers Report' ,
                                subheader = 'President' ,
                                content = 'No Report' ,
                                ),
                 MeetingMinutes(datetime = datetime.datetime(2013,4,28),
                                header = 'Officers Report' ,
                                subheader = 'Vice-President' ,
                                content = 'Something' ,
                                ),
                 MeetingMinutes(datetime = datetime.datetime(2013,4,28),
                                header = 'Officers Report' ,
                                subheader = 'Chief Line Officer' ,
                                content = 'Nothing at all' ,
                                ),
                 MeetingMinutes(datetime = datetime.datetime(2013,4,28),
                                header = 'Committee Report' ,
                                subheader = 'Website Committee' ,
                                content = 'We are doing great things' ,
                                ),
                 MeetingMinutes(datetime = datetime.datetime(2013,4,28),
                                header = 'New Business' ,
                                subheader = 'New Quarters' ,
                                content = 'Probably not gonna happen' ,
                                ),
                 MeetingMinutes(datetime = datetime.datetime(2013,4,28),
                                header = 'Announcements' ,
                                subheader = 'MCI' ,
                                content = 'Be prepared' ,
                                ),
                 MeetingMinutes(datetime = datetime.datetime(2013,4,21),
                                header = 'Officers Report' ,
                                subheader = 'President' ,
                                content = 'week before:No Report' ,
                                ),
                 MeetingMinutes(datetime = datetime.datetime(2013,4,21),
                                header = 'Officers Report' ,
                                subheader = 'Vice-President' ,
                                content = 'week before:Something' ,
                                ),
                 MeetingMinutes(datetime = datetime.datetime(2013,4,21),
                                header = 'Officers Report' ,
                                subheader = 'Chief Line Officer' ,
                                content = 'week before:Nothing at all' ,
                                ),
                 MeetingMinutes(datetime = datetime.datetime(2013,4,21),
                                header = 'Committee Report' ,
                                subheader = 'Website Committee' ,
                                content = 'week before:We are doing great things' ,
                                ),
                 MeetingMinutes(datetime = datetime.datetime(2013,4,21),
                                header = 'New Business' ,
                                subheader = 'New Quarters' ,
                                content = 'week before:Probably not gonna happen' ,
                                ),
                 MeetingMinutes(datetime = datetime.datetime(2013,4,21),
                                header = 'Announcements' ,
                                subheader = 'MCI' ,
                                content = 'week before:Be prepared' ,
                                ),
                        ])
        DBSession.add_all(
                [
                    Pictures(picture='eqpt1.jpg',description="", category="Equipment"),
                    Pictures(picture='eqpt2.jpg',description="", category="Equipment"),
                    Pictures(picture='eqpt3.jpg',description="", category="Equipment"),
                    Pictures(picture='eqpt4.jpg',description="", category="Equipment"),
                    Pictures(picture='eqpt5.jpg',description="", category="Equipment"),
                    Pictures(picture='mock1.jpg',description="", category="2004 Mock DWI"),
                    Pictures(picture='mock2.jpg',description="", category="2004 Mock DWI"),
                    Pictures(picture='mock3.jpg',description="", category="2004 Mock DWI"),
                    Pictures(picture='mock4.jpg',description="", category="2004 Mock DWI"),
                    Pictures(picture='mock5.jpg',description="", category="2004 Mock DWI"),
                    Pictures(picture='mock6.jpg',description="", category="2004 Mock DWI"),
                    Pictures(picture='mock7.jpg',description="", category="2004 Mock DWI"),
                    Pictures(picture='mock8.jpg',description="", category="2004 Mock DWI"),
                    Pictures(picture='mock9.jpg',description="", category="2004 Mock DWI"),
                    Pictures(picture='mock10.jpg',description="", category="2004 Mock DWI"),
                    Pictures(picture='mock11.jpg',description="", category="2004 Mock DWI"),
                    Pictures(picture='mock12.jpg',description="", category="2004 Mock DWI"),
                    Pictures(picture='mock13.jpg',description="", category="2004 Mock DWI"),
                    Pictures(picture='mock14.jpg',description="", category="2004 Mock DWI"),
                    Pictures(picture='mock15.jpg',description="", category="2004 Mock DWI"),
                    Pictures(picture='mock16.jpg',description="", category="2004 Mock DWI"),
                    Pictures(picture='2005mockdwi1.jpg',description="", category="2005 Mock DWI"),
                    Pictures(picture='2005mockdwi2.jpg',description="", category="2005 Mock DWI"),
                    Pictures(picture='2005mockdwi3.jpg',description="", category="2005 Mock DWI"),
                    Pictures(picture='2005mockdwi4.jpg',description="", category="2005 Mock DWI"),
                    Pictures(picture='2005mockdwi5.jpg',description="", category="2005 Mock DWI"),
                    Pictures(picture='carsmash1.jpg', description="", category="Car Smash Fundraiser"),
                    Pictures(picture='carsmash2.jpg', description="", category="Car Smash Fundraiser"),
                    Pictures(picture='carsmash3.jpg', description="", category="Car Smash Fundraiser"),
                    Pictures(picture='carsmash4.jpg', description="", category="Car Smash Fundraiser"),
                    Pictures(picture='carsmash5.jpg', description="", category="Car Smash Fundraiser"),
                    Pictures(picture='wellnessfair1.jpg', description="", category="2006 Wellness Fair"),
                    Pictures(picture='wellnessfair2.jpg', description="", category="2006 Wellness Fair"),
                    Pictures(picture='wellnessfair4.jpg', description="", category="2006 Wellness Fair"),
                ])

        DBSession.add_all(
                [
                    DutyCrews(crewnumber=0, username='turdona193'),
                    DutyCrews(crewnumber=1, username='muehlbjp193'),
                    DutyCrews(crewnumber=2, username='guarintb193')
                ])

