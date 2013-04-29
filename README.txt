## Start virtual Environment

    $ virtualenv .
    
## Activate Virtual Environment

    $ source bin/activate

## Install pyramid + nose + coverage

    $ easy_install pyramid nose coverage

## Make project from scaffold alchemy

    $ pcreate -s alchemy rescueweb

## Install project in development mode

    $ cd rescueweb
    $ python setup.py develop

## Run tests (tests are a good thing!)
    
    $ python setup.py test -q

## Run test with coverage
    
    $ nosetests --cover-package=tutorial --cover-erase --with-coverage

## Change model.py and initializedb.py to store new tables

    $ initialize_rescueweb_db development.ini

## Launch project
    
    $ pserve development.ini --reload
