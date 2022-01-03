from flask import make_response
import connexion
from ..services.helper_functions import *
from flask_jwt_extended import jwt_required, get_jwt_identity


def read_all(id):
    return query(
        "SELECT replies.replyid, replies.announcementid, replies.timestamp, replies.userid, users.first_name, "
        "users.last_name, replies.content FROM replies JOIN users "
        "ON replies.userid = users.userid "
        "WHERE replies.announcementid = %(id)s "
        "ORDER BY replies.timestamp ASC", {'id': id})


@jwt_required()
def post(id):
    try:
        body = connexion.request.json['reply']
        content = body['content']
    except KeyError:
        return response("Invalid body", 404)
    query_update(
        "INSERT INTO replies (announcementid, userid, content) VALUES (%(id)s, %(userid)s, %(content)s)",
        {'id': id, 'userid': get_jwt_identity(), 'content': content})
    return response("Reply to announcement={announcementid} successfully posted".format(announcementid=str(id)),
                    200)


def edit(id):
    is_int(id)
    try:
        body = connexion.request.json['reply']
        content = body['content']
    except KeyError:
        return response("Invalid body", 404)

    query_update(
        "UPDATE replies SET content=%(content)s WHERE replyid=%(id)s",
        {'id': id, 'content': content})
    return response("Reply {id} successfully edited".format(id=str(id)), 200)


def delete(id):
    is_int(id)
    query_update("DELETE FROM replies WHERE replyid =%(id)s", {'id': id})
    return response("{id} successfully deleted".format(id=str(id)), 200)
