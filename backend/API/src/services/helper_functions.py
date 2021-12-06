from .db import engine
from mysql.connector import Error
from flask import make_response, abort
import re


def query(query, param):
    with engine.connect() as connection:
        result = connection.exec_driver_sql(query, param)
        return [dict(zip(result.keys(), value)) for value in result]


def query_update(query, param):
    with engine.connect() as connection:
        connection.exec_driver_sql(query, param)


def is_int(value):
    if not re.compile("[0-9]").match(value):
        incorrect_input()


def is_boolean(value):
    try:
        if int(value) == 0 or int(value) == 1:
            return
    except:
        print()
    incorrect_input()


def incorrect_input():
    abort(404, "Incorrect input")
