import connexion
from flask_jwt_extended import get_jwt_identity, jwt_required
from ..services.helper_functions import *

from ..services.permissions import Announcements
from ..services.permissions.permissions import check_permissions, check_jwt


@check_permissions(Announcements.may_read)
def read_one(announcement_id):
    
    return query(
        "SELECT announcements.announcementid, announcements.timestamp, announcements.userid, users.first_name, "
        "users.last_name, announcements.title, announcements.content "
        "FROM announcements JOIN users ON announcements.userid = users.userid "
        "WHERE announcements.announcementid = %(id)s "
        "ORDER BY announcements.timestamp DESC", {'id': announcement_id})


@check_jwt()
def read_global():
    return query(
        "SELECT announcements.announcementid, announcements.timestamp, announcements.userid, users.first_name, "
        "users.last_name, announcements.title, announcements.content FROM announcements JOIN users "
        "ON announcements.userid = users.userid "
        "WHERE announcements.projectid IS NULL "
        "ORDER BY announcements.timestamp DESC", None)


@check_permissions(Announcements.may_create_global)
def create_global():
    try:
        body = connexion.request.json['announcement']
        title = body['title']
        content = body['content']
    except KeyError:
        return response("Invalid body", 400)
    query_update(
        "INSERT INTO announcements (userid, projectid, title, content) VALUES (%(userid)s, NULL, %(title)s, "
        "%(content)s)",
        {'userid': get_jwt_identity(), 'content': content, 'title': title})
    return response("Global Announcement successfully posted", 200)


@check_permissions(Announcements.may_update_delete)
def update(announcement_id):
    
    try:
        body = connexion.request.json['announcement']
        title = body['title']
        content = body['content']
    except KeyError:
        return response("Invalid body", 400)
    query_update(
        "UPDATE announcements SET title=%(title)s, content=%(content)s WHERE announcementid=%(id)s",
        {'id': announcement_id, 'content': content, 'title': title})
    return response(f"Announcement {announcement_id} successfully edited", 200)


@check_permissions(Announcements.may_update_delete)
def delete(announcement_id):
    
    query_update("DELETE FROM announcements WHERE announcementid = %(id)s", {'id': announcement_id})
    return response(f"{announcement_id} successfully deleted", 200)


@check_permissions(Announcements.may_read_reply)
def read_replies(announcement_id):
    
    return query(
        "SELECT replies.replyid, replies.announcementid, replies.timestamp, replies.userid, users.first_name, "
        "users.last_name, replies.content FROM replies JOIN users "
        "ON replies.userid = users.userid "
        "WHERE replies.announcementid = %(announcementid)s "
        "ORDER BY replies.timestamp ASC", {'announcementid': announcement_id})


@check_permissions(Announcements.may_add_reply)
def add_reply(announcement_id):
    try:
        body = connexion.request.json['reply']
        content = body['content']
    except KeyError:
        return response("Invalid body", 400)
    query_update(
        "INSERT INTO replies (announcementid, userid, content) VALUES (%(id)s, %(userid)s, %(content)s)",
        {'id': announcement_id, 'userid': get_jwt_identity(), 'content': content})
    return response(f"Reply to announcement={announcement_id} successfully posted", 200)
