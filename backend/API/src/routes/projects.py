from flask import make_response
from ..services.helper_functions import *


def read_all():
    return query("select * from projects")


def read_one(id):
    is_int(id)
    return query("select * from projects where projectid=%(id)s", {'id': id})


def update(id, isarchived):
    is_int(id)
    is_boolean(isarchived)
    query_update("UPDATE projects SET isarchived =%(isarchived)s where projectid=%(id)s",
                 {'id': id, 'isarchived': str(int(isarchived))})
    return make_response("{id} successfully updated".format(id=str(id)), 200)


def delete(id):
    is_int(id)
    query_update("DELETE FROM projects WHERE projectid =%(id)s", {'id': id})
    return make_response("{id} successfully deleted".format(id=str(id)), 200)
