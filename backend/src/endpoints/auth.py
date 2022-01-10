import connexion
import datetime
import src.config as config
from flask import jsonify
from src.services.helper_functions import query, query_update, response
from flask_jwt_extended import jwt_required, \
    create_access_token, create_refresh_token, get_jwt_identity, set_access_cookies, \
    set_refresh_cookies, unset_jwt_cookies, verify_jwt_in_request
from src.services.permissions.permissions import check_jwt
from ..services.extensions import bcrypt


def login():
    try:
        email = connexion.request.form['username']
        send_password = connexion.request.form['password']
    except KeyError:
        return response("Invalid body", 400)

    user = query("SELECT * FROM users WHERE email =%(email)s",
                 {'email': email})
    if len(user) == 0:
        return response("Wrong password or username", 401)
    user = user[0]

    if int(user['failed_login_count']) >= config.ATTEMPTS_BEFORE_COOLDOWN:
        if int((datetime.datetime.now() - user['last_failed_login']).total_seconds()) > config.COOLDOWN_TIME_SECONDS:
            query_update("UPDATE users SET failed_login_count = 0 where userid = %(userid)s",
                         {'userid': user['userid']})
        else:
            return response("Acces Denied, your account is blocked for " +
                            str(config.COOLDOWN_TIME_SECONDS - int((datetime.datetime.now() - user[
                                'last_failed_login']).total_seconds())) +
                            " more seconds", 401)
    try:
        if bcrypt.check_password_hash(user['password_hash'], send_password):
            access_token = create_access_token(identity=user['userid'])
            dict = query("SELECT * FROM roles WHERE roleid=%(roleid)s", {'roleid': user['roleid']})
            dict[0]['userid'] = user['userid']
            dict[0]['first_name'] = user['first_name']
            dict[0]['last_name'] = user['last_name']
            dict[0]['screening_status'] = user['screening_status']
            resp = jsonify(dict)  # TODO: misschien niet alle permissies dumpen?
            set_access_cookies(resp, access_token)
            return resp, 200
    except ValueError:
        print('Password format incorrect')
    query_update("UPDATE users SET last_failed_login = NOW(), failed_login_count = failed_login_count + 1 WHERE "
                 "userid = %(userid)s", {'userid': user['userid']})
    return response("Wrong password or username", 401)


@check_jwt()
def logout():
    resp = jsonify({'logout': True})
    unset_jwt_cookies(resp)
    return resp, 200


@check_jwt()
def change_password():
    user_id = get_jwt_identity()
    user = query("SELECT * FROM users WHERE userid =%(userid)s", {'userid': user_id()})[0]
    try:
        if bcrypt.check_password_hash(user['password_hash'], connexion.request.form['old_password']):
            password = connexion.request.form['new_password']
            validate_password(password)
            password = bcrypt.generate_password_hash(password).decode('utf-8')
            query_update(
                "UPDATE users SET password_hash=%(password_hash)s "
                "WHERE userid=%(userid)s",
                {"password_hash": password, "userid": user_id})
            return response(f"User {user_id} successfully updated", 200)
        return response("Incorrect current password", 401)
    except KeyError:
        return response("Invalid body", 400)


def validate_password(password):
    if len(password) > config.MAX_PASSWORD_LENGTH:
        response('Password length exceeded max length of ' + config.MAX_PASSWORD_LENGTH, 400)
    if len(password) < config.MIN_PASSWORD_LENGTH:
        response('Password must be at least ' + config.MAX_PASSWORD_LENGTH + "characters long", 400)
