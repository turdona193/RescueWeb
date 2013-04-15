USERS = {'turdona193':'nick',
          'muehlbjp193':'jared',
          'guarintb193' :'tim'}
GROUPS = {'turdona' :['group:Member'],
          'muehlbjp193':['group:admin'],
          'guarintb193':['group:admin']}

def groupfinder(userid, request):
    if userid in USERS:
        return GROUPS.get(userid, [])