from flask import make_response
from ..services.helper_functions import *


def read_all():
    return query("SELECT projectid, project_name, description, is_archived, created, last_updated FROM projects")


def read_one(id):
    is_int(id)
    return query("SELECT projectid, project_name, description, is_archived, created, last_updated FROM projects WHERE projectid = %(id)s", {'id': id})


def update(id, is_archived):
    is_int(id)
    is_boolean(is_archived)
    query_update("UPDATE projects SET is_archived =%(is_archived)s where projectid=%(id)s",
                 {'id': id, 'is_archived': str(int(is_archived))})
    return make_response("{id} successfully updated".format(id=str(id)), 200)


def delete(id):
    is_int(id)
    query_update("DELETE FROM projects WHERE projectid =%(id)s", {'id': id})
    return make_response("{id} successfully deleted".format(id=str(id)), 200)
