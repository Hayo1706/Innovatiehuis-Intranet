from backend.API.db import cur,connection
from flask import make_response, abort


def read_all():
    cur.execute("select * from projects")
    row_headers = [x[0] for x in cur.description]
    rv = cur.fetchall()
    return [dict(zip(row_headers, result)) for result in rv]


def read_one(projectid):
    cur.execute("select * from projects where projectid=" + projectid)
    row_headers = [x[0] for x in cur.description]
    rv = cur.fetchall()
    if len(rv) > 0:
        return [dict(zip(row_headers, result)) for result in rv]
    else:
        return abort(404, "Could not find project with id= {projectid}".format(projectid=projectid))


def update(projectid, isarchived):
    read_one(projectid)
    cur.execute("UPDATE projects SET isarchived = "+str(int(isarchived))+" where projectid=" + projectid)
    connection.commit()
    return make_response("{projectid} successfully updated".format(projectid=projectid), 200)


def delete(projectid):
    read_one(projectid)
    cur.execute("DELETE FROM projects WHERE projectid = " + projectid)
    connection.commit()
    return make_response("{projectid} successfully deleted".format(projectid=projectid), 200)
