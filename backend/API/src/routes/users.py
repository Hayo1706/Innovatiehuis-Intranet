from ..services.helper_functions import *


def read_all():
    return query("select * from users")


def read_one(id):
    return query("select * from users where userid= %(id)s", {'id': id})


def read_user_projects(id):
    return query("SELECT * FROM users_has_projects INNER JOIN projects ON "
                 "users_has_projects.projectid = projects.projectid "
                 "WHERE users_has_projects.userid = %(id)s AND projects.isarchived = 0", {'id': id})


def delete(id):
    is_int(id)
    query_update("DELETE FROM users WHERE userid =%(id)s", {'id': id})
    return make_response("{id} successfully deleted".format(id=str(id)), 200)
