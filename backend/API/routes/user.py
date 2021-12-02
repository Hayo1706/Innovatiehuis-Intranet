from API.helper_functions import *


def read_all():
    return query("select * from users")


def read_user_projects(id):
    user_exists(id)
    return query("SELECT * FROM user_has_projects INNER JOIN projects ON "
                "user_has_projects.projectid=projects.projectid"
                " WHERE userid = " + id + " AND projects.isarchived = 0")