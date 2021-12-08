from flask import make_response
import connexion
from ..services.helper_functions import *


def read_all(id):
    return query(
        "SELECT replies.replyid, replies.announcementid, replies.timestamp, replies.userid, users.firstname, "
        "users.lastname, replies.content FROM replies JOIN users "
        "ON replies.userid = users.userid "
        "WHERE replies.announcementid = %(id)s "
        "ORDER BY replies.timestamp ASC", {'id': id})


def post(id):
    body = connexion.request.json['reply']
    query_update(
        "INSERT INTO replies (announcementid, userid, content) VALUES (%(id)s, %(userid)s, %(content)s)",
        {'id': id, 'userid': body['userid'], 'content': body['content']})
    return make_response("Reply to announcement={announcementid} successfully posted".format(announcementid=str(id)), 200)


def edit(id):
    is_int(id)
    body = connexion.request.json['reply']
    query_update(
        "UPDATE replies SET content=%(content)s WHERE announcementid=%(id)s",
        {'id': id, 'content': body['content']})
    return make_response("Reply to announcement={announcementid} successfully edited".format(announcementid=str(id)), 200)


def delete(id):
    is_int(id)
    query_update("DELETE FROM replies WHERE replyid =%(id)s", {'id': id})
    return make_response("{id} successfully deleted".format(id=str(id)), 200)
