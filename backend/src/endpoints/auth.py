import connexion
import datetime
import src.config as config
from flask import  jsonify
from src.services.helper_functions import query, query_update, response

from flask_jwt_extended import jwt_required, \
    create_access_token, create_refresh_token, get_jwt_identity, set_access_cookies, \
    set_refresh_cookies, unset_jwt_cookies, verify_jwt_in_request

JWT_ISSUER = 'innovatieplatform'
JWT_SECRET = 'kiZn04wb0XEPfpnkTbgmFtHtNElRThM2nWNdD51KaosfRT8HzVLqPB3UMnKPwb1'  # TODO Change This? Moet Secret om de zo veel tijd gerefreshed worden?
JWT_LIFETIME_SECONDS = config.SESSION_LIFETIME_SECONDS
JWT_ALGORITHM = 'HS256'

ATTEMPTS_BEFORE_COOLDOWN = config.ATTEMPTS_BEFORE_COOLDOWN
COOLDOWN_TIME_SECONDS = config.COOLDOWN_TIME_SECONDS


def login():
    return generate_token()


# TODO: gooi merendeel van deze logica in een JWT service

def generate_token():
    try:
        email = connexion.request.form['username']
        send_password = connexion.request.form['password']
    except KeyError:
        return response("Invalid body", 404)

    user = query("SELECT * FROM users WHERE email =%(email)s",
                 {'email': email})
    if len(user) == 0:
        return response("Wrong password or username", 401)
    user = user[0]

    if int(user['failed_login_count']) >= ATTEMPTS_BEFORE_COOLDOWN:
        if int((datetime.datetime.now() - user['failed_login_count']).total_seconds()) > COOLDOWN_TIME_SECONDS:
            query_update("UPDATE users SET failed_login_count = 0 where userid = %(userid)s",
                         {'userid': user['userid']})
        else:
            return response("Acces Denied, your account is blocked for " +
                                 str(int((datetime.datetime.now() - user[
                                     'last_failed_login']).total_seconds()) - ATTEMPTS_BEFORE_COOLDOWN) +
                                 " more seconds", 401)
    if not user['password_hash'] == send_password:
        query_update("UPDATE users SET last_failed_login = NOW(), failed_login_count = failed_login_count + 1 where "
                     "userid = %(userid)s", {'userid': user['userid']})
        return response("Wrong password or username", 401)
    access_token = create_access_token(identity=user['userid'])

    dict = query("SELECT may_read_all_projects, may_read_all_users, may_delete_all_projects FROM roles where "
                 "roleid=%(roleid)s", {'roleid': user['roleid']})
    dict[0]['userid'] = user['userid']
    resp = jsonify(dict) #TODO meer permissies
    set_access_cookies(resp, access_token)
    return resp, 200
