from flask import request
from .extensions import db


def query(query, param=None):
    with db.engine.connect() as connection:
        result = connection.exec_driver_sql(query, param)
        return [dict(zip(result.keys(), value)) for value in result]


def query_update(query, param=None):
    with db.engine.connect() as connection:
        connection.exec_driver_sql(query, param)


def response(message, code=200, **arguments):
    data = {'response': {'resource': request.path, 'message': message}}
    for key, value in arguments.items():
        data['response'][key] = value
    return data, code


def is_boolean(value):
    try:
        if int(value) == 0 or int(value) == 1:
            return
    except:
        print()
    response("Incorrect input", 404)
