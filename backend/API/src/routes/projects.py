from flask import make_response
from ..services.helper_functions import *


def read_all():
    return query("SELECT first_project_id AS projectid, first_name AS `name`,firstisarchived AS  isarchived, firstcreatedat AS createdat, firstlastupdated AS lastupdated,  `name`AS parentname, projectid AS parentid,amountsubprojects FROM (SELECT projectid AS first_project_id, `name` AS first_name, isarchived AS firstisarchived, createdat AS firstcreatedat, lastupdated AS firstlastupdated, amountsubprojects, parentid FROM (SELECT projectid, NAME, isarchived, createdat, lastupdated, COUNT(childid) AS `amountsubprojects` FROM projects LEFT JOIN projects_has_parents ON projects.projectid = projects_has_parents.parentid GROUP BY projectid) AS newprojects LEFT JOIN projects_has_parents ON projects_has_parents.childid = newprojects.projectid) AS projectswithparentid LEFT JOIN projects ON projectswithparentid.parentid = projects.projectid")


def read_one(id):
    is_int(id)
    return query("SELECT first_project_id AS projectid, first_name AS `name`,firstisarchived AS  isarchived, firstcreatedat AS createdat, firstlastupdated AS lastupdated,  `name`AS parentname, projectid AS parentid,amountsubprojects FROM (SELECT projectid AS first_project_id, `name` AS first_name, isarchived AS firstisarchived, createdat AS firstcreatedat, lastupdated AS firstlastupdated, amountsubprojects, parentid FROM (SELECT projectid, NAME, isarchived, createdat, lastupdated, COUNT(childid) AS `amountsubprojects` FROM projects LEFT JOIN projects_has_parents ON projects.projectid = projects_has_parents.parentid GROUP BY projectid) AS newprojects LEFT JOIN projects_has_parents ON projects_has_parents.childid = newprojects.projectid) AS projectswithparentid LEFT JOIN projects ON projectswithparentid.parentid = projects.projectid WHERE projectid=%(id)s", {'id': id})


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
