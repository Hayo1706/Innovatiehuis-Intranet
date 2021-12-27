import connexion

from ..services.helper_functions import *


def read_all():
    return query("SELECT userid, firstname, lastname, email, roleid,`name` AS rolename, screeningstatus, createdat, COUNT(projectid) AS amountprojects, IFNULL(MAX(lastseen),createdat) AS lastseen FROM (SELECT * FROM users LEFT JOIN roles USING(roleid)) as users LEFT JOIN users_has_projects USING(userid) GROUP BY userid")


def read_one(id):
    return query("SELECT userid, firstname, lastname, email, roleid,`name` AS rolename, screeningstatus, createdat, COUNT(projectid) AS amountprojects, IFNULL(MAX(lastseen),createdat) AS lastseen FROM (SELECT * FROM users LEFT JOIN roles USING(roleid)) as users LEFT JOIN users_has_projects USING(userid) GROUP BY userid where userid= %(id)s", {'id': id})


def read_user_projects(id):
    return query("SELECT * FROM users_has_projects INNER JOIN projects ON "
                 "users_has_projects.projectid = projects.projectid "
                 "WHERE users_has_projects.userid = %(id)s AND projects.isarchived = 0", {'id': id})


def delete(id):
    is_int(id)
    query_update("DELETE FROM users WHERE userid =%(id)s", {'id': id})
    return make_response("{id} successfully deleted".format(id=str(id)), 200)

def post():
    try:
        body = connexion.request.json
        firstname = body['firstname']
        lastname = body['lastname']
        email = body['email']
        roleid = body['roleid']
        screeningstatus = body['screeningstatus']
    except KeyError:
        return make_response("Invalid body", 404)

    query_update(
        "INSERT INTO users (firstname, lastname, email, roleid, screeningstatus) VALUES (%(firstname)s, %(lastname)s, %(email)s, %(roleid)s, %(screeningstatus)s)",
        {'firstname': firstname, 'lastname': lastname, 'email': email, 'roleid': roleid, 'screeningstatus': screeningstatus})
    return make_response("User successfully added", 200)

