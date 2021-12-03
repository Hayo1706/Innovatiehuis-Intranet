from API.helper_functions import *
from flask import make_response, abort


def read_all(id):
    project_exists(id)
    return query("SELECT announcements.announcementid, announcements.timestamp, announcements.userid, users.firstname, users.lastname, announcements.title, announcements.content FROM announcements JOIN users "
                 "ON announcements.userid = users.userid "
                 "WHERE announcements.projectid = " + str(id) +
                 " ORDER BY announcements.timestamp DESC")


#TODO fix dit
def post(id):
    project_exists(id)
    query_update("INSERT INTO announcements (userid, projectid, title, content) VALUES (1, " + str(id) + ", 'nieuwe mededeling', 'AAAAAAAAAAAAA.')")
    return make_response("Announcement in project={projectid} successfully posted".format(projectid=str(id)), 200)


def delete(id):
    announcement_exists(id)
    query_update("DELETE FROM announcements WHERE announcementid = " + str(id))
    return make_response("{announcement} successfully deleted".format(announcement=str(id)), 200)
