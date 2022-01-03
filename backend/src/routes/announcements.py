import connexion
from flask import make_response
from ..services.helper_functions import *
from flask_jwt_extended import jwt_required, get_jwt_identity


def read_global_announcements():
    return query(
        "SELECT announcements.announcementid, announcements.timestamp, announcements.userid, users.first_name, "
        "users.last_name, announcements.title, announcements.content FROM announcements JOIN users "
        "ON announcements.userid = users.userid "
        "WHERE announcements.projectid IS NULL "
        "ORDER BY announcements.timestamp DESC", None)


def read_all(id):
    return query(
        "SELECT announcements.announcementid, announcements.timestamp, announcements.userid, users.first_name, "
        "users.last_name, announcements.title, announcements.content FROM announcements JOIN users "
        "ON announcements.userid = users.userid "
        "WHERE announcements.projectid = %(id)s"
        " ORDER BY announcements.timestamp DESC", {'id': id})


@jwt_required()
def post_global():
    try:
        body = connexion.request.json['announcement']
        title = body['title']
        content = body['content']
    except KeyError:
        return response("Invalid body", 404)
    query_update(
        "INSERT INTO announcements (userid, projectid, title, content) VALUES (%(userid)s, NULL, %(title)s, "
        "%(content)s)",
        {'userid': get_jwt_identity(), 'content': content, 'title': title})
    return response("Global Announcement successfully posted".format(projectid=str(id)), 200)


@jwt_required()
def post(id):
    is_int(id)
    try:
        body = connexion.request.json['announcement']
        title = body['title']
        content = body['content']
    except KeyError:
        return response("Invalid body", 404)

    query_update(
        "INSERT INTO announcements (userid, projectid, title, content) VALUES (%(userid)s, %(id)s, %(title)s, "
        "%(content)s)",
        {'userid': get_jwt_identity(), 'id': id, 'content': content, 'title': title})
    return response("Announcement in project={projectid} successfully posted".format(projectid=str(id)), 200)


def delete(id):
    is_int(id)
    query_update("DELETE FROM announcements WHERE announcementid = %(id)s", {'id': id})
    return response("{announcement} successfully deleted".format(announcement=str(id)), 200)


def edit(id):
    is_int(id)
    try:
        body = connexion.request.json['announcement']
        title = body['title']
        content = body['content']
    except KeyError:
        return response("Invalid body", 404)
    query_update(
        "UPDATE announcements SET title=%(title)s, content=%(content)s WHERE announcementid=%(id)s",
        {'id': id, 'content': content, 'title': title})
    return response("Announcement in project={projectid} successfully edited".format(projectid=str(id)), 200)
