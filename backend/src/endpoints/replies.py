import connexion
from ..services.helper_functions import *


def update(reply_id):
    is_int(reply_id)
    try:
        body = connexion.request.json['reply']
        content = body['content']
    except KeyError:
        return response("Invalid body", 404)

    query_update(
        "UPDATE replies SET content=%(content)s WHERE replyid=%(id)s",
        {'id': reply_id, 'content': content})
    return response(f"Reply {reply_id} successfully edited", 200)


def delete(reply_id):
    is_int(reply_id)
    query_update("DELETE FROM replies WHERE replyid =%(id)s", {'id': id})
    return response(f"Reply {reply_id} successfully deleted", 200)
