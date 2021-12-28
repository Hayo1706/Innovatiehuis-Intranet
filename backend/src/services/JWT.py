import time
import connexion
import six
import datetime
from flask import abort, make_response
from werkzeug.exceptions import Unauthorized
from .helper_functions import query, query_update
# from flask_login import LoginManager, UserMixin, login_user
from jose import JWTError, jwt
from .extensions import login_manager


JWT_ISSUER = 'innovatieplatform'
JWT_SECRET = 'change_this'  # TODO Change This
JWT_LIFETIME_SECONDS = 600
JWT_ALGORITHM = 'HS256'

ATTEMPTS_BEFORE_COOLDOWN = 6
COOLDOWN_TIME_SECONDS = 60

#
# @login_manager.user_loader
# def load_user(user_id):
#     return check_db(user_id).get_id()


def check_db(userid):
    # query database just so we can pass an object to the callback
    user = query("SELECT firstname, lastname, roleid,userid WHERE userid=%(userid)s", {'userid': userid})[0]
    object = User(user['firstname'], user['lastname'], user['roleid'], user['userid'], active=True)
    if object.id == userid:
        return object
    else:
        return None


def generate_token():
    try:
        email = connexion.request.form['username']
        send_password = connexion.request.form['password']
    except KeyError:
        return make_response("Invalid body", 404)

    user = query("SELECT * FROM users WHERE email =%(email)s",
                 {'email': email})
    if len(user) == 0:
        return make_response("Wrong password or username", 401)
    user = user[0]

    if int(user['wrongpasswordcount']) >= ATTEMPTS_BEFORE_COOLDOWN:
        if int((datetime.datetime.now() - user['lastwrongpassword']).total_seconds()) > COOLDOWN_TIME_SECONDS:
            query_update("UPDATE users SET wrongpasswordcount = 0 where userid = %(userid)s",
                         {'userid': user['userid']})
        else:
            return make_response("Acces Denied, your account is blocked for " +
                                 str(int((datetime.datetime.now() - user[
                                     'lastwrongpassword']).total_seconds()) - ATTEMPTS_BEFORE_COOLDOWN) +
                                 " more seconds", 401)
    if not user['hash'] == send_password:
        query_update("UPDATE users SET lastwrongpassword = NOW(),wrongpasswordcount = wrongpasswordcount + 1 where "
                     "userid = %(userid)s", {'userid': user['userid']})
        return make_response("Wrong password or username", 401)
    object = User(user['firstname'], user['lastname'], user['roleid'], user['userid'], active=True)
    # login_user(object)
    timestamp = _current_timestamp()
    payload = {
        "iss": JWT_ISSUER,
        "iat": int(timestamp),
        "exp": int(timestamp + JWT_LIFETIME_SECONDS),
        "sub": str(id),
        "scope": str('admin')  # TODO Change this
    }
    return {'access_token': jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM), 'token_type': "bearer"}


def decode_token(token):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except JWTError as e:
        six.raise_from(Unauthorized, e)


def _current_timestamp() -> int:
    return int(time.time())


class User():
    def __init__(self, firstname, lastname, roleid, id, active=True):
        self.firstname = firstname
        self.lastname = lastname
        self.roleid = roleid
        self.id = id
        self.active = active

    def is_active(self):
        return self.active