from sqlalchemy import (
    Column,
    Integer,
    Text,
    Float,
    ForeignKey,
    Date,
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
                (Allow, 'group:Member', 'Member'),
                (Allow, 'group:admin' ,  ALL_PERMISSIONS) ]
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

    
    
    