from flask import request
from .extensions import db
import re


def query(query, param=None):
    with db.engine.connect() as connection:
        result = connection.exec_driver_sql(query, param)
        return [dict(zip(result.keys(), value)) for value in result]


def query_update(query, param=None):
    with db.engine.connect() as connection:
        connection.exec_driver_sql(query, param)


def is_int(value):
    if not re.compile("[0-9]").match(value):
        response("Incorrect input", 404)


def response(message, code=200):
    data = {'response': {'resource': request.path, 'message': message}}
    return data, code


def is_boolean(value):
    try:
        if int(value) == 0 or int(value) == 1:
            return
    except:
        print()
    response("Incorrect input", 404)
