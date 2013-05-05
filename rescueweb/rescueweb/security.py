from pyramid.security import (
    unauthenticated_userid,
    )

from .models import (
    DBSession,
    Users,
    Privileges,
    )

def get_user(request):
    """Gets the username and the groups the user is associated with"""
    userid = unauthenticated_userid(request),
    if userid:
        # This should return None if the user doesn't exist in the database
        return DBSession.query(
                    Users.username,
                    Users.fullname,
                    Users.birthday,
                    Users.street,
                    Users.city,
                    Users.state,
                    Users.zipcode,
                    Users.residence,
                    Users.roomnumber,
                    Users.phonenumber,
                    Users.email,
                    Privileges.privilege,
                    Privileges.pyramidsecuritygroup).\
                    join(Privileges).\
                    filter(Users.username == userid[0]).first()

def groupfinder(userid, request):
    """Returns every security group a username is associated with.

    This function is called when a user is logging in. If the username exists in
    the Users table, then return a list of that username's permission groups. 

    """
    user = request.user
    if user:
        return [user.pyramidsecuritygroup]
