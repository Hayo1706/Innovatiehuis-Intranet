import connexion
from ..services.helper_functions import *

from ..services.permissions import Announcements
from ..services.permissions.permissions import check_permissions


@check_permissions(Announcements.may_update_delete_reply)
def update(reply_id):
    try:
        body = connexion.request.json['reply']
        content = body['content']
    except KeyError:
        return response("Foute aanvraag", 400)

    query_update(
        "UPDATE replies SET content=%(content)s WHERE replyid=%(id)s",
        {'id': reply_id, 'content': content})
    return response(f"Reply {reply_id} successfully edited", 200)


@check_permissions(Announcements.may_update_delete_reply)
def delete(reply_id):
    query_update("DELETE FROM replies WHERE replyid=%(id)s", {'id': reply_id})
    return response(f"Reply {reply_id} successfully deleted", 200)
