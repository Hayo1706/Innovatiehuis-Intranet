import time

import connexion
import six
from werkzeug.exceptions import Unauthorized
from ..services.helper_functions import *
import datetime

from jose import JWTError, jwt

JWT_ISSUER = 'innovatieplatform'
JWT_SECRET = 'change_this'  # TODO Change This
JWT_LIFETIME_SECONDS = 600
JWT_ALGORITHM = 'HS256'

ATTEMPTS_BEFORE_COOLDOWN = 6
COOLDOWN_TIME_SECONDS = 60


def generate_token():
    try:
        email = connexion.request.form['username']
        send_password = connexion.request.form['password']
    except KeyError:
        return make_response("Invalid body", 404)

    user = query("SELECT lastwrongpassword,wrongpasswordcount,hash,userid FROM users WHERE email =%(email)s",
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


def get_secret(user, token_info) -> str:
    return '''
    You are user_id {user} and the secret is 'wbevuec'.
    Decoded token claims: {token_info}.
    '''.format(user=user, token_info=token_info)


def _current_timestamp() -> int:
    return int(time.time())
