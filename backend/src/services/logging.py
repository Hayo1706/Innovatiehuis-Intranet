import json
import traceback
from datetime import datetime, timezone

import connexion
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from flask_jwt_extended.exceptions import NoAuthorizationError
from jwt import ExpiredSignatureError

from src.services.helper_functions import query


# TODO Niels has to send the logging message to ElasticStack, maybe change it to his liking a bit first

def log_response_and_request(request, response):
    try:
        verify_jwt_in_request()
        uid = get_jwt_identity()
    except (ExpiredSignatureError, NoAuthorizationError):
        uid = None

    request_str = request.data.decode("utf-8")
    response_obj = {}

    # if response is no file
    if not response.direct_passthrough:
        response_str = response.data.decode("utf-8")
        try:
            response_obj = json.loads(response_str)
        except:
            response_obj = {}

    response_message = ""
    if type(response_obj) == dict and "message" in response_obj.keys():
        response_message = response_obj["message"]

    request_username = ""
    if "username" in connexion.request.form.keys():
        request_username = " , username=" + connexion.request.form["username"]

    log_date = datetime.now().strftime("%d-%m-%Y")

    if not uid:
        user = None
    else:
        user_data = query("SELECT first_name, last_name, email FROM users WHERE userid=" + str(uid) + ";")[0]
        name = user_data["first_name"] + " " + user_data["last_name"]
        user = {"id": uid, "name": name, "email": user_data["email"]}

    log_object = dict()
    log_object["Date"] = log_date
    log_object["User"] = user
    log_object["Action"] = request.method + " " + request.path
    log_object["IP Address"] = request.remote_addr
    log_object["Request"] = request_str + request_username

    if response.status_code == 500:
        log_object["Response"] = response.status
        log_object["Traceback"] = response_message
    else:
        log_object["Response"] = response.status + " " + response_message

    log_message = json.dumps(log_object)

    print(log_message)
