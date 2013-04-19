#LoginIns table still needs to be added along with the dutycrew stuff

from sqlalchemy import (
    Column,
    Integer,
    Text,
    Float,
    ForeignKey,
    Date,
    DateTime,
    Boolean,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

from pyramid.security import (
    Allow,
    Everyone,
    ALL_PERMISSIONS,
    )
class RootFactory(object):
    __acl__ = [ (Allow,  Everyone     , 'Guest'),
                (Allow, 'Member', 'Member'),
                (Allow, 'admin' ,  ALL_PERMISSIONS) ]
    def __init__(self, request):
        pass

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Page(Base):
    """ The SQLAlchemy declarative model class for a Page object. """
    __tablename__ = 'pages'
    name = Column(Text, primary_key = True)
    data = Column(Text)

    def __init__(self, name, data):
        self.name = name
        self.data = data
        
class Announcements(Base):
    __tablename__ = 'announcements'
    key = Column(Integer, primary_key=True)
    header = Column(Text)
    text = Column(Text)
    priority = Column(Integer, ForeignKey('Privileges.privilegevalue'))
    username = Column(Text,ForeignKey('Users.username'))
    
    def __init__(self,key, header, text, priority, username):
        self.key = key
        self.header = header
        self.text  = text
        self.priority = priority
        self.username = username
        
class Documents(Base):
    __tablename__ = 'documents'
    name = Column(Text)
    fileName = Column(Text, primary_key = True)
    
    def __init__(self, name, fileName):
        self.name = name
        self.fileName = fileName
        
        
class users(Base):
    __tablename__ = 'Users'
    username = Column(Text, primary_key=True)
    password = Column(Text)
    firstname = Column(Text)
    middlename = Column(Text)
    lastname = Column(Text)
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
    trainingvalue = Column(Integer, ForeignKey('TrainingLevels.trainingvalue'))
    administrativevalue = Column(Integer, ForeignKey('AdministrativeStatus.administrativevalue'))
    operationalvalue = Column(Integer, ForeignKey('OperationalStatus.operationalvalue'))
    portablenumber = Column(Integer)
    
    def __init__(self, username, password,firstname,middlename,lastname,birthday,street,city,
                 state,zipcode,residence,roomnumber,phonenumber,email,privileges,
                 trainingvalue,administrativevalue,operationalvalue,portablenumber):
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
        
class emtcert(Base):
    __tablename__ = 'EMTCertification'
    username = Column(Text, ForeignKey('Users.username'), primary_key=True)
    certnumber = Column(Integer)

    def __init__(self, username,certnumber):
        self.username = username
        self.certnumber = certnumber
        
class certifications(Base):
    __tablename__ = 'Certifications'
    username = Column(Text, ForeignKey('Users.username'), primary_key=True)
    certification = Column(Text, primary_key=True)
    expiration = Column(Text)

    def __init__(self, username,certification,expiration):
        self.username = username
        self.certification = certification
        self.expiration = expiration
        
class operationalstatus(Base):
    __tablename__ = 'OperationalStatus'
    operationalvalue = Column(Integer, primary_key=True)
    status = Column(Text)

    def __init__(self, operationalvalue,status):
        self.operationalstatus = operationalvalue
        self.status = status
        
class administrativestatus(Base):
    __tablename__ = 'AdministrativeStatus'
    administrativevalue = Column(Integer, primary_key=True)
    status = Column(Text)

    def __init__(self, administrativevalue,status):
        self.administrativestatus = administrativevalue
        self.status = status
        
class eboardpositions(Base):
    __tablename__ = 'Position'
    position = Column(Text, primary_key=True)
    username = Column(Text, ForeignKey('Users.username'))

    def __init__(self, position,username):
        self.position = position
        self.username = username
      
class traininglevel(Base):
    __tablename__ = 'TrainingLevels'
    trainingvalue = Column(Integer, primary_key=True)
    traininglevel = Column(Text)
    
    def __init__(self, trainingvalue, traininglevel):
        self.trainingvalue = trainingvalue
        self.traininglevel = traininglevel
        
class privileges(Base):
    __tablename__ = 'Privileges'
    privilegevalue = Column(Integer, primary_key=True)
    privilege = Column(Text)
    
    def __init__(self, privilegevalue, privilege):
        self.privilegevalue = privilegevalue
        self.privilege = privilege

class weblinks(Base):
    __tablename__ = 'Links'
    name = Column(Text, primary_key=True)
    address = Column(Text)
    
    def __init__(self, name, address):
        self.name = name
        self.address = address

class standBy(Base):
    __tablename__ = 'StandBy'
    standbyid = Column(Integer, primary_key=True)
    event = Column(Text)
    location = Column(Text)
    notes = Column(Text)
    startdatetime = Column(DateTime)
    enddatetime = Column(DateTime)

    def __init__(self, standbyid, event, location, notes, startdatetime,
                 enddatetime):
        self.standbyid = standbyid
        self.event = event
        self.location = location
        self.notes = notes
        self.startdatetime = startdatetime
        self.enddatetime = enddatetime
    
class standByPersonnel(Base):
    __tablename__ = 'StandByPersonnel'
    standbyid = Column(Integer, ForeignKey('StandBy.standbyid'), primary_key=True)
    username = Column(Text, ForeignKey('Users.username'), primary_key=True)
    standbyposition = Column(Text)
    coverrequested = Column(Boolean)
    covered = Column(Text, ForeignKey('Users.username'))

    def __init__(self, standbyid, username, standbyposition, coverrequested, covered):
        self.standbyid = standbyid
        self.username = username
        self.standbyposition = standbyposition
        self.coverrequested = coverrequested
        self.covered = covered

class crewChiefSchedule(Base):
    __tablename__ = 'CrewChiefSchedule'
    date = Column(Date, primary_key=True)
    ccusername = Column(Text, ForeignKey('Users.username'))
    pccusername = Column(Text, ForeignKey('Users.username'))

    def __init__(self, date, ccusername, pccusername):
        self.date = date
        self.ccusername = ccusername
        self.pccusername = pccusername

class events(Base):
    __tablename__ = 'Events'
    eventid = Column(Integer, primary_key=True)
    startdatetime = Column(DateTime)
    enddatetime = Column(DateTime)
    name = Column(Text)
    notes = Column(Text)
    privileges = Column(Integer, ForeignKey('Privileges.privilegevalue'))

    def __init__(self, eventid, startdatetime, enddatetime, name, notes, privileges):
        self.eventid = eventid
        self.startdatetime = startdatetime
        self.enddatetime = enddatetime
        self.name = name
        self.notes = notes
        self.privileges = privileges

class attendees(Base):
    __tablename__ = 'Attendees'
    eventid = Column(Integer, ForeignKey('Events.eventid'), primary_key=True)
    username = Column(Text, ForeignKey('Users.username'), primary_key=True)

    def __init__(self, eventid, username):
        self.eventid = eventid
        self.username = username

class meetingMinutes(Base):
    __tablename__ = 'MeetingMinutes'
    meetingindex = Column(Integer, primary_key=True)
    datetime = Column(DateTime)

    def __init__(self, eventid, username):
        self.meetingindex = meetingindex
        self.datetime = datetime

class minutesContent(Base):
    __tablename__ = 'MinutesContent'
    meetingindex = Column(Integer, ForeignKey('MinutesContent.meetingindex'), primary_key=True)
    header = Column(Text, primary_key=True)
    subheader = Column(Text, primary_key=True)
    content = Column(Text)

    def __init__(Base, meetingindex, header, subheader, content):
        self.meetingindex = meetingindex
        self.header = header
        self.subheader = subheader
        self.content = content







