from flask import make_response
from ..services.helper_functions import *


def read_all(id):
    return query(
        "SELECT replies.replyid, replies.announcementid, replies.timestamp, replies.userid, users.firstname, "
        "users.lastname, replies.content FROM replies JOIN users "
        "ON replies.userid = users.userid "
        "WHERE replies.announcementid = %(id)s "
        "ORDER BY replies.timestamp ASC", {'id': id})


def delete(id):
    is_int(id)
    query_update("DELETE FROM replies WHERE replyid =%(id)s", {'id': id})
    return make_response("{id} successfully deleted".format(id=str(id)), 200)
