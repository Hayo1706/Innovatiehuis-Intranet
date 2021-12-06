from ..services.helper_functions import *


def read_all():
    return query("select * from users")


def read_one(id):
    return query("select * from users where userid= %(id)s", {'id': id})


def read_user_projects(id):
    return query("SELECT * FROM user_has_projects INNER JOIN projects ON "
                 "user_has_projects.projectid=projects.projectid"
                 " WHERE userid =  %(id)s AND projects.isarchived = 0", {'id': id})
