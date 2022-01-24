import connexion
import datetime
import src.config as config
from flask import jsonify, request
from src.services.helper_functions import query, query_update, response
from flask_jwt_extended import jwt_required, \
    create_access_token, create_refresh_token, get_jwt_identity, set_access_cookies, \
    set_refresh_cookies, unset_jwt_cookies, verify_jwt_in_request
from src.services.permissions.permissions import check_jwt
from ..services.extensions import bcrypt
from itsdangerous import URLSafeSerializer
import re

def login():
    try:
        email = connexion.request.form['username']
        send_password = connexion.request.form['password']
        authenticator_code = connexion.request.form['authenticator_code']
   
    except KeyError:
        return response("Foute aanvraag", 400)

    user = query("SELECT * FROM users WHERE email =%(email)s",
                 {'email': email})
    if len(user) == 0:
        return response("Incorrect wachtwoord of gebruikersnaam", 401)
    user = user[0]

    if int(user['failed_login_count']) >= config.ATTEMPTS_BEFORE_COOLDOWN:
        if int((datetime.datetime.now() - user['last_failed_login']).total_seconds()) > config.COOLDOWN_TIME_SECONDS:
            query_update("UPDATE users SET failed_login_count = 0 where userid = %(userid)s",
                         {'userid': user['userid']})
        else:
            return response("Toegang geweigerd, je account is geblokkeerd voor " +
                            str(config.COOLDOWN_TIME_SECONDS - int((datetime.datetime.now() - user[
                                'last_failed_login']).total_seconds())) +
                            " seconden", 401)
    try:
        if bcrypt.check_password_hash(user['password_hash'], send_password):
            access_token = create_access_token(identity=user['userid'])
            dict = query("SELECT * FROM roles WHERE roleid=%(roleid)s", {'roleid': user['roleid']})
            dict[0]['userid'] = user['userid']
            dict[0]['first_name'] = user['first_name']
            dict[0]['last_name'] = user['last_name']
            dict[0]['screening_status'] = user['screening_status']
            # TODO: misschien niet alle permissies dumpen?
            rsp = {'resource': request.path, 'code': 200, 'message': 'Succes', 'result': dict}
            rsp = jsonify(rsp)
            set_access_cookies(rsp,access_token)
            return rsp, 200
    except ValueError:
        print('Password format incorrect')
    query_update("UPDATE users SET last_failed_login = NOW(), failed_login_count = failed_login_count + 1 WHERE "
                 "userid = %(userid)s", {'userid': user['userid']})
    return response("Incorrect wachtwoord of gebruikersnaam", 401)


def logout():
    resp = jsonify({'logout': True})
    unset_jwt_cookies(resp)
    return resp, 200


def change_password():
    token = connexion.request.args.get('resettoken')
    old_password = connexion.request.form['old_password']
    new_password = connexion.request.form['new_password']
    if len(old_password) == 0 and len(token) > 0:
        serializer = URLSafeSerializer(config.PASSWORD_CHANGE_SECRET_KEY)
        data = serializer.loads(token)
        try:
            return first_time_password(data[1], new_password, data[0])
        except Exception:
            response('Fout bij het veranderen van wachtwoord', 400)
    else:
        return change_existing_password(old_password, new_password)


def first_time_password(old_password, new_password, user_id):
    user = query("SELECT * FROM users WHERE userid =%(userid)s", {'userid': user_id})[0]
    if user['password_hash'] == old_password:
        return set_password(new_password, user_id)
    return response("Incorrect wachtwoord", 401)


@check_jwt()
def change_existing_password(old_password, new_password):
    user_id = get_jwt_identity()
    try:
        user = query("SELECT * FROM users WHERE userid =%(userid)s", {'userid': user_id})[0]
        if bcrypt.check_password_hash(user['password_hash'], old_password):
            return set_password(new_password, user_id)
        return response("Incorrect wachtwoord ", 401)
    except KeyError:
        return response("Foute aanvraag", 400)


def set_password(password, user_id):
    """
    Verify the strength of 'password'
    Returns a dict indicating the wrong criteria
    A password is considered strong if:
        8 characters length or more
        1 digit or more
        1 symbol or more
        1 uppercase letter or more
        1 lowercase letter or more
    """

    # calculating the length
    if len(password) > config.MAX_PASSWORD_LENGTH:
        return response('Wachtwoord te lang, maximale lengte is  ' + str(config.MAX_PASSWORD_LENGTH) + ' karakters', 400)
    if len(password) < config.MIN_PASSWORD_LENGTH:
        return response('Wachtwoord te kort, minimale lengte is ' + str(config.MAX_PASSWORD_LENGTH) + "karakters", 400)

    # searching for digits
    if config.FORCE_NUMBERS and re.search(r"\d", password) is None:
        return response('Wachtwoord voldoet niet aan eisen: Minimaal 1 cijfer',400)

    # searching for uppercase
    if config.FORCE_CAPITAL_LETTERS and re.search(r"[A-Z]", password) is None:
        return response('Wachtwoord voldoet niet aan eisen: Minimaal 1 hoofdletter',400)

    # searching for lowercase
    if re.search(r"[a-z]", password) is None:
        return response('Wachtwoord voldoet niet aan eisen: Minimaal 1 kleine letter',400)

    # searching for symbols
    if config.FORCE_SPECIAL_CHARACTER and re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password) is None:
        return response('Wachtwoord voldoet niet aan eisen: Minimaal 1 speciaal karakter: !,@,#,$,%,^,&, etc.. ',400)

    query_update(
        "UPDATE users SET password_hash=%(password_hash)s "
        "WHERE userid=%(userid)s",
        {"password_hash": bcrypt.generate_password_hash(password).decode('utf-8'), "userid": user_id})
    return response("Wachtwoord veranderd",200)
