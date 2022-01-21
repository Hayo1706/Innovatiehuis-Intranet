from flask import request
from .extensions import db


def query(query, param=None):
    with db.engine.connect() as connection:
        result = connection.exec_driver_sql(query, param)
        return [dict(zip(result.keys(), value)) for value in result]


def query_update(query, param=None):
    with db.engine.connect() as connection:
        connection.exec_driver_sql(query, param)


def response(message, code=200, data = None):
    rsp = {'resource': request.path, 'message': message, 'data': data}
    if not code == 200:
        rsp['code'] = code
    return rsp, code


def is_boolean(value):
    try:
        if int(value) == 0 or int(value) == 1:
            return
    except:
        print()
    response("Incorrect input", 404)
