import json
from datetime import datetime, timezone

import connexion



# TODO Niels has to send the logging message to ElasticStack, maybe change it to his liking a bit first
def log_response_and_request(request, response, uid):
    response_str = ""
    request_str = request.data.decode("utf-8")
    response_obj = {}

    # if response is no file
    if not response.direct_passthrough:
        response_str = response.data.decode("utf-8")
        response_obj = json.loads(response_str)

    response_message = ""
    if type(response_obj) == dict and "message" in response_obj.keys():
        response_message = response_obj["message"]

    request_username = ""
    if "username" in connexion.request.form.keys():
        request_username = " , username=" + connexion.request.form["username"]

    uid_message = "\nNo user is logged in\n"
    if uid:
        uid_message = "\nUser is logged in. Id of the user: " + str(uid) + "\n"

    response_time = datetime.now().strftime("%Y-%m-%d %H:%M")

    log_message = "\nRequest  - url : {request_url} , method: {request_method}" \
                  " , body: {request_body} {request_username}\n" \
                  "Response - status : {response_code} , message: {response_message}" \
                  "{uid_message}" \
                  "Time of the response: {response_time}\n" \
        .format(request_url=request.url, request_method=request.method, request_body=request_str,
                request_username=request_username,
                response_code=response.status,
                response_message=response_message, uid_message=uid_message, response_time=response_time)

    print(log_message)
