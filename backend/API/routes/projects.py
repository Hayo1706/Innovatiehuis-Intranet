from API.helper_functions import *
from flask import make_response, abort


def read_all():
    return query("select * from projects")


def read_one(id):
    project_exists(id)
    return query("select * from projects where projectid=" + str(id))


def update(id, isarchived):
    project_exists(id)
    query_update("UPDATE projects SET isarchived = " + str(int(isarchived)) + " where projectid=" + str(id))
    return make_response("{id} successfully updated".format(id=str(id)), 200)


def delete(id):
    project_exists(id)
    query_update("DELETE FROM projects WHERE projectid = " + id)
    return make_response("{id} successfully deleted".format(id=str(id)), 200)
