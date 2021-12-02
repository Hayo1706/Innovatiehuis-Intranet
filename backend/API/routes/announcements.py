from backend.API.db import cur, connection
from flask import make_response, abort


def project_exists(projectid):
    cur.execute("SELECT * FROM projects where projectid=" + projectid)
    rv = cur.fetchall()
    if len(rv) > 0:
        return True
    if project_exists(projectid):
        abort(404, "Could not find specified projects")


def read_all(projectid):
    project_exists(projectid)
    cur.execute("SELECT * FROM announcements JOIN users ON announcements.userid = users.userid WHERE announcements.projectid = " + projectid + " ORDER BY announcements.timestamp DESC")
    row_headers = [x[0] for x in cur.description]
    rv = cur.fetchall()
    return [dict(zip(row_headers, result)) for result in rv]

def post(projectid):
    project_exists(projectid)
    cur.execute("INSERT INTO announcements (userid, projectid, title, content) VALUES (1, " + projectid + ", 'nieuwe mededeling', 'AAAAAAAAAAAAA.')")
    connection.commit()
    return make_response("Announcement in project={projectid} successfully posted".format(projectid=projectid), 200)