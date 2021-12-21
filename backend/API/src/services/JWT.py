import time

import connexion
import six
from werkzeug.exceptions import Unauthorized
from ..services.helper_functions import *


from jose import JWTError, jwt

JWT_ISSUER = 'innovatieplatform'
JWT_SECRET = 'change_this'
JWT_LIFETIME_SECONDS = 600
JWT_ALGORITHM = 'HS256'


def generate_token():
    try:
        dict = connexion.request.json['loginAttempt']
        email = dict['email']
        send_password = dict['password']
    except KeyError:
        return make_response("Invalid body", 404)

    id = query("SELECT userid FROM users WHERE email =%(email)s", {'email': email})
    if len(id) == 0:
        return make_response("Wrong password or username", 401)

    id = id[0]['userid']
    password = query("SELECT hash FROM users WHERE userid =%(id)s", {'id': id})[0]['hash']
    if not password == send_password:
        return make_response("Wrong password or username", 401)

    timestamp = _current_timestamp()
    payload = {
        "iss": JWT_ISSUER,
        "iat": int(timestamp),
        "exp": int(timestamp + JWT_LIFETIME_SECONDS),
        "sub": str(id),
        "scope": str('admin')
    }

    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


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