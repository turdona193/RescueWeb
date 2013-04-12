import os
import sys
import transaction

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from ..models import (
    DBSession,
    users,
    emtcert,
    certifications,
    operationalstatus,
    administrativestatus,
    eboardpositions,
    traininglevel,
    privileges,
    Page,
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
        model = Page(name = 'Home', data = 'The SUNY Potsdam Campus Rescue Squad started in 1992 as a group of college students that formed together to provide much needed medical coverage for SUNY Potsdam varsity athletic events as well as various other college events.')
        DBSession.add(model)
        
        model = Page(name = 'History', data = 'This is where the history of the Squad would be')
        DBSession.add(model)
        
        user = users(username = 'turdona193', password = 'nick',firstname = 'Nicholas',middlename = 'Anthony',lastname = 'Turdo',
                     street = '3510 Barrington Dr',city = 'Potsdam', state = 'NY',zipcode = '13676',residence = 'Townhouse',roomnumber = 'A1-104',
                     phonenumber = 6462595690,email = 'turdona193@potsdam.edu',privileges = 2,trainingvalue = 3,administrativevalue = 3,operationalvalue = 4, portablenumber = 10)
        DBSession.add(user)
        user = users(username = 'muehlbjp193', password = 'jared',firstname = 'Jared',middlename = 'Paul',lastname = 'Muehlbauer',
                     street = '2512 Barrington Dr',city = 'Potsdam', state = 'NY',zipcode = '13676',residence = 'Townhouse',roomnumber = 'A1-201',
                     phonenumber = 6462595690,email = 'muehlbjp193@potsdam.edu',privileges = 2,trainingvalue = 3,administrativevalue = 4,operationalvalue = 6, portablenumber = 7)
        DBSession.add(user)
        user = users(username = 'guarintb193', password = 'tim',firstname = 'Tim',middlename = 'Bret',lastname = 'Guarino',
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
