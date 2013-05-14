from sqlalchemy import (
    Column,
    Integer,
    Text,
    Float,
    ForeignKey,
    Date,
    DateTime,
    Boolean,
    TIMESTAMP,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    column_property,
    )

from zope.sqlalchemy import ZopeTransactionExtension

from pyramid.security import (
    Allow,
    Everyone,
    ALL_PERMISSIONS,
    )

class RootFactory(object):
    __acl__ = [ (Allow,  Everyone     , 'Guest'),
                (Allow, 'member', 'Member'),
                (Allow, 'admin' ,  ALL_PERMISSIONS) ]
    def __init__(self, request):
        pass

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class Page(Base):
    """ The SQLAlchemy declarative model class for a Page object. """
    __tablename__ = 'Pages'
    name = Column(Text, primary_key = True)
    data = Column(Text)

    def __init__(self, name, data):
        self.name = name
        self.data = data
        
class Announcements(Base):
    __tablename__ = 'Announcements'
    key = Column(Integer, primary_key=True)
    header = Column(Text)
    text = Column(Text)
    priority = Column(Integer, ForeignKey('Privileges.privilegevalue'))
    username = Column(Text,ForeignKey('Users.username'))
    posted = Column(TIMESTAMP)
    
    def __init__(self, header, text, priority, username,posted):
        self.header = header
        self.text  = text
        self.priority = priority
        self.username = username
        self.posted = posted
        
class Documents(Base):
    __tablename__ = 'Documents'
    name = Column(Text)
    filename = Column(Text, primary_key = True)
    
    def __init__(self, name, filename):
        self.name = name
        self.filename = filename
        
        
class Users(Base):
    __tablename__ = 'Users'
    username = Column(Text, primary_key=True)
    password = Column(Text)
    firstname = Column(Text)
    middlename = Column(Text)
    lastname = Column(Text)
    fullname = column_property(firstname + " " + lastname)
    birthday = Column(Date)
    street = Column(Text)
    city =Column(Text)
    state = Column(Text)
    zipcode = Column(Integer)
    residence = Column(Text)
    roomnumber = Column(Text)
    phonenumber = Column(Integer)
    email = Column(Text)
    privileges = Column(Integer, ForeignKey('Privileges.privilegevalue'))
    trainingvalue = Column(Integer, ForeignKey('TrainingLevel.trainingvalue'))
    administrativevalue = Column(Integer, ForeignKey('AdministrativeStatus.administrativevalue'))
    operationalvalue = Column(Integer, ForeignKey('OperationalStatus.operationalvalue'))
    portablenumber = Column(Integer)
    
    def __init__(self, username, password, firstname, middlename, lastname,
            birthday, street, city, state, zipcode, residence, roomnumber,
            phonenumber, email, privileges, trainingvalue, administrativevalue,
            operationalvalue, portablenumber):
        self.username = username
        self.password = password
        self.firstname =firstname
        self.middlename = middlename
        self.lastname = lastname
        self.birthday = birthday
        self.street = street
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.residence = residence
        self.roomnumber = roomnumber
        self.phonenumber = phonenumber
        self.email = email
        self.privileges = privileges
        self.trainingvalue = trainingvalue
        self.administrativevalue = administrativevalue
        self.operationalvalue = operationalvalue
        self.portablenumber = portablenumber
        
   
class Certifications(Base):
    __tablename__ = 'Certifications'
    username = Column(Text, ForeignKey('Users.username'), primary_key=True)
    certification = Column(Text, primary_key=True)
    certnumber = Column(Integer)
    expiration = Column(Text)

    def __init__(self, username,certification,certnumber,expiration):
        self.username = username
        self.certification = certification
        self.certnumber = certnumber
        self.expiration = expiration
        
class OperationalStatus(Base):
    __tablename__ = 'OperationalStatus'
    operationalvalue = Column(Integer, primary_key=True)
    status = Column(Text)

    def __init__(self, operationalvalue,status):
        self.operationalstatus = operationalvalue
        self.status = status
        
class AdministrativeStatus(Base):
    __tablename__ = 'AdministrativeStatus'
    administrativevalue = Column(Integer, primary_key=True)
    status = Column(Text)

    def __init__(self, administrativevalue,status):
        self.administrativestatus = administrativevalue
        self.status = status
        
class EboardPositions(Base):
    __tablename__ = 'EboardPosition'
    eboardposition = Column(Text, primary_key=True)
    username = Column(Text, ForeignKey('Users.username'))

    def __init__(self,eboardposition,username):
        self.eboardposition = eboardposition
        self.username = username
      
class TrainingLevel(Base):
    __tablename__ = 'TrainingLevel'
    trainingvalue = Column(Integer, primary_key=True)
    traininglevel = Column(Text)
    
    def __init__(self, trainingvalue, traininglevel):
        self.trainingvalue = trainingvalue
        self.traininglevel = traininglevel
        
class Privileges(Base):
    __tablename__ = 'Privileges'
    privilegevalue = Column(Integer, primary_key=True)
    privilege = Column(Text)
    pyramidsecuritygroup = Column(Text)
    
    def __init__(self, privilegevalue, privilege, pyramidsecuritygroup):
        self.privilegevalue = privilegevalue
        self.privilege = privilege
        self.pyramidsecuritygroup = pyramidsecuritygroup

class WebLinks(Base):
    __tablename__ = 'Links'
    name = Column(Text, primary_key=True)
    address = Column(Text)
    
    def __init__(self, name, address):
        self.name = name
        self.address = address

class StandBy(Base):
    __tablename__ = 'StandBy'
    standbyid = Column(Integer, primary_key=True)
    event = Column(Text)
    location = Column(Text)
    notes = Column(Text)
    startdatetime = Column(DateTime)
    enddatetime = Column(DateTime)

    def __init__(self, event, location, notes, startdatetime,
                 enddatetime):
        self.event = event
        self.location = location
        self.notes = notes
        self.startdatetime = startdatetime
        self.enddatetime = enddatetime
    
class StandByPersonnel(Base):
    __tablename__ = 'StandByPersonnel'
    standbyid = Column(Integer, ForeignKey('StandBy.standbyid'), primary_key=True)
    username = Column(Text, ForeignKey('Users.username'), primary_key=True)
    standbyposition = Column(Text)
    coverrequested = Column(Boolean)

    def __init__(self, standbyid, username, standbyposition, coverrequested):
        self.standbyid = standbyid
        self.username = username
        self.standbyposition = standbyposition
        self.coverrequested = coverrequested

class CrewChiefSchedule(Base):
    __tablename__ = 'CrewChiefSchedule'
    date = Column(Date, primary_key=True)
    ccusername = Column(Text, ForeignKey('Users.username'))
    pccusername = Column(Text, ForeignKey('Users.username'))

    def __init__(self, date, ccusername, pccusername):
        self.date = date
        self.ccusername = ccusername
        self.pccusername = pccusername

class Events(Base):
    __tablename__ = 'Events'
    eventid = Column(Integer, primary_key=True)
    startdatetime = Column(DateTime)
    enddatetime = Column(DateTime)
    name = Column(Text)
    notes = Column(Text)
    location = Column(Text)
    privileges = Column(Integer, ForeignKey('Privileges.privilegevalue'))

    def __init__(self, startdatetime, enddatetime, name, notes, location, privileges):
        self.startdatetime = startdatetime
        self.enddatetime = enddatetime
        self.name = name
        self.notes = notes
        self.location = location
        self.privileges = privileges

class Attendees(Base):
    __tablename__ = 'Attendees'
    eventid = Column(Integer, ForeignKey('Events.eventid'), primary_key=True)
    username = Column(Text, ForeignKey('Users.username'), primary_key=True)

    def __init__(self, eventid, username):
        self.eventid = eventid
        self.username = username

class MeetingMinutes(Base):
    __tablename__ = 'MeetingMinutes'
    meetingindex = Column(Integer, primary_key=True)
    datetime = Column(DateTime)
    header = Column(Text)
    subheader = Column(Text)
    content = Column(Text)

    def __init__(self, datetime, header, subheader, content):
        self.datetime = datetime
        self.header = header
        self.subheader = subheader
        self.content = content

class Pictures(Base):
    __tablename__ = 'Pictures'
    pictureindex = Column(Integer, primary_key=True)
    picture = Column(Text)
    description = Column(Text)
    category = Column(Text)
    def __init__(self, picture, description, category):
        self.picture = picture
        self.description = description
        self.category = category
        
class DutyCrews(Base):
    __tablename__ = 'Duty_Crews'
    crewnumber = Column(Integer, primary_key=True)
    username = Column(Text, ForeignKey('Users.username'), primary_key=True)
    def __init__(self, crewnumber, username):
        self.crewnumber = crewnumber
        self.username = username
        
class DutyCrewCalendar(Base):
    __tablename__ = 'Duty_Crew_Calendar'
    day = Column(Date, primary_key = True)
    crewnumber = Column(Integer,ForeignKey('Duty_Crews.crewnumber'))
    def __init__(self,day,crewnumber):
        self.day = day
        self.crewnumber = crewnumber
        
class DutyCrewSchedule(Base):
    __tablename__ = 'Duty_Crew_Schedule'
    day = Column(Date, primary_key = True)
    username = Column(Text, ForeignKey('Users.username'), primary_key=True)
    coveragerequest = Column(Boolean)
    def __init__(self,day,username,coveragerequest):
        self.day = day
        self.username = username
        self.coveragerequest = coveragerequest
        
class LoginIns(Base):
    __tablename__ = 'Login_Ins'
    username = Column(Text, ForeignKey('Users.username'), primary_key=True)
    TSTAMP = Column(TIMESTAMP, primary_key=True)

