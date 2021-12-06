import connexion
from flask import make_response
from ..services.helper_functions import *


def read_global_announcements():
    return query(
        "SELECT announcements.announcementid, announcements.timestamp, announcements.userid, users.firstname, "
        "users.lastname, announcements.title, announcements.content FROM announcements JOIN users "
        "ON announcements.userid = users.userid "
        "WHERE announcements.projectid IS NULL "
        "ORDER BY announcements.timestamp DESC", None)


def read_all(id):
    return query(
        "SELECT announcements.announcementid, announcements.timestamp, announcements.userid, users.firstname, "
        "users.lastname, announcements.title, announcements.content FROM announcements JOIN users "
        "ON announcements.userid = users.userid "
        "WHERE announcements.projectid = %(id)s"
        " ORDER BY announcements.timestamp DESC", {'id': id})


def post_global():
    body = connexion.request.json
    query_update(
        "INSERT INTO announcements (userid, projectid, title, content) VALUES (5, NULL, %(content)s, %(title)s)",
        {'content': body['content'], 'title': body['title']})
    return make_response("Announcement in project={projectid} successfully posted".format(projectid=str(id)), 200)


# TODO fix dit zodat correcte user wordt ingeschreven
def post(id):
    is_int(id)
    body = connexion.request.json
    query_update(
        "INSERT INTO announcements (userid, projectid, title, content) VALUES (5, %(id)s, %(content)s, %(title)s)",
        {'id': id, 'content': body['content'], 'title': body['title']})
    return make_response("Announcement in project={projectid} successfully posted".format(projectid=str(id)), 200)


def delete(id):
    is_int(id)
    query_update("DELETE FROM announcements WHERE announcementid = %(id)s", {'id': id})
    return make_response("{announcement} successfully deleted".format(announcement=str(id)), 200)
