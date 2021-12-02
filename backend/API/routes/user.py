from backend.API.db import cur
from flask import abort


def read_all():
    cur.execute("select * from users")
    row_headers = [x[0] for x in cur.description]
    rv = cur.fetchall()
    return [dict(zip(row_headers, result)) for result in rv]


def read_user_projects(userid):
    cur.execute("SELECT * FROM user_has_projects INNER JOIN projects ON "
                "user_has_projects.projectid=projects.projectid"
                " WHERE userid = " + userid+" AND projects.isarchived = 0")
    row_headers = [x[0] for x in cur.description]
    rv = cur.fetchall()
    if len(rv) > 0:
        return [dict(zip(row_headers, result)) for result in rv]
    else:
        return abort(404, "Could not find project with id= {userid}".format(userid=userid))