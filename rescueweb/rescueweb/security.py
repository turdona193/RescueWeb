USERS = {'turdona193':'nick',
          'muehlbjp193':'jared',
          'guarintb193' :'tim'}
GROUPS = {'turdona193' :['Member'],
          'muehlbjp193':['admin'],
          'guarintb193':['admin']}

def groupfinder(userid, request):
    if userid in USERS:
        return GROUPS.get(userid, [])