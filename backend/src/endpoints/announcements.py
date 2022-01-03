import connexion
from ..services.helper_functions import *
from flask_jwt_extended import get_jwt_identity


def read_one(announcement_id):
    is_int(announcement_id)
    return query(
        "SELECT announcements.announcementid, announcements.timestamp, announcements.userid, users.first_name, "
        "users.last_name, announcements.title, announcements.content "
        "FROM announcements JOIN users ON announcements.userid = users.userid "
        "WHERE announcements.announcementid = %(id)s "
        "ORDER BY announcements.timestamp DESC", {'id': announcement_id})


def read_global():
    return query(
        "SELECT announcements.announcementid, announcements.timestamp, announcements.userid, users.first_name, "
        "users.last_name, announcements.title, announcements.content FROM announcements JOIN users "
        "ON announcements.userid = users.userid "
        "WHERE announcements.projectid IS NULL "
        "ORDER BY announcements.timestamp DESC", None)


def create_global():
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
    return response("Global Announcement successfully posted", 200)


def update(announcement_id):
    is_int(announcement_id)
    try:
        body = connexion.request.json['announcement']
        title = body['title']
        content = body['content']
    except KeyError:
        return response("Invalid body", 404)
    query_update(
        "UPDATE announcements SET title=%(title)s, content=%(content)s WHERE announcementid=%(id)s",
        {'id': announcement_id, 'content': content, 'title': title})
    return response(f"Announcement {announcement_id} successfully edited", 200)


def delete(announcement_id):
    is_int(announcement_id)
    query_update("DELETE FROM announcements WHERE announcementid = %(id)s", {'id': announcement_id})
    return response(f"{announcement_id} successfully deleted", 200)


def read_replies(announcement_id):
    is_int(announcement_id)
    return query(
        "SELECT replies.replyid, replies.announcementid, replies.timestamp, replies.userid, users.first_name, "
        "users.last_name, replies.content FROM replies JOIN users "
        "ON replies.userid = users.userid "
        "WHERE replies.announcementid = %(id)s "
        "ORDER BY replies.timestamp ASC", {'id': announcement_id})


def add_reply(announcement_id):
    try:
        body = connexion.request.json['reply']
        content = body['content']
    except KeyError:
        return response("Invalid body", 404)
    query_update(
        "INSERT INTO replies (announcementid, userid, content) VALUES (%(id)s, %(userid)s, %(content)s)",
        {'id': announcement_id, 'userid': get_jwt_identity(), 'content': content})
    return response(f"Reply to announcement={announcement_id} successfully posted", 200)
