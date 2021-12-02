from .db import cur, connection
from flask import make_response, abort


def query(query):
    cur.execute(query)
    row_headers = [x[0] for x in cur.description]
    rv = cur.fetchall()
    return [dict(zip(row_headers, result)) for result in rv]


def query_update(query):
    cur.execute(query)
    connection.commit()


def exists(query):
    cur.execute(query)
    rv = cur.fetchall()
    if len(rv) > 0:
        return True
    abort(404, "Could not find specified id")


def project_exists(projectid):
    exists("SELECT * FROM projects where projectid=" + projectid)


def user_exists(userid):
    exists("SELECT * FROM users where userid=" + userid)


def announcement_exists(announcementid):
    exists("SELECT * FROM announcements where announcementid=" + announcementid)
