from .db import connection_pool
from mysql.connector import Error
from flask import make_response, abort


def query(query):
    try:
        connection = connection_pool.get_connection()
        if connection.is_connected():
            cur = connection.cursor()
            cur.execute(query)
            rv = cur.fetchall()

    except Error as e:
        print(e)
        abort(404, "Error while connecting to database")
    finally:
        row_headers = [x[0] for x in cur.description]
        cur.close()
        connection.close()
        return [dict(zip(row_headers, result)) for result in rv]


def query_update(query):
    try:
        connection = connection_pool.get_connection()
        if connection.is_connected():
            cur = connection.cursor()
            cur.execute(query)
    except Error as e:
        print(e)
        abort(404, "Error while connecting to database")
    finally:
        connection.commit()
        cur.close()
        connection.close()


def exists(query):
    try:
        connection = connection_pool.get_connection()
        if connection.is_connected():
            cur = connection.cursor()
            cur.execute(query)
            rv = cur.fetchall()


    except Error as e:
        print(e)
        abort(404, "Error while connecting to database")
    finally:
        cur.close()
        connection.close()
        if len(rv) > 0:
            return True
        abort(404, "Could not find specified id")


def project_exists(projectid):
    exists("SELECT * FROM projects where projectid=" + str(projectid))


def user_exists(userid):
    exists("SELECT * FROM users where userid=" + str(userid))


def announcement_exists(announcementid):
    exists("SELECT * FROM announcements where announcementid=" + str(announcementid))
