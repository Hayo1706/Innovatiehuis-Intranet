import connexion
import datetime
from flask import abort, make_response, jsonify
from .helper_functions import query, query_update

from flask_jwt_extended import jwt_required, \
    create_access_token, create_refresh_token, get_jwt_identity, set_access_cookies, \
    set_refresh_cookies, unset_jwt_cookies, verify_jwt_in_request

JWT_ISSUER = 'innovatieplatform'
JWT_SECRET = 'kiZn04wb0XEPfpnkTbgmFtHtNElRThM2nWNdD51KaosfRT8HzVLqPB3UMnKPwb1'  # TODO Change This? Moet Secret om de zo veel tijd gerefreshed worden?
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

    user = query("SELECT * FROM users WHERE email =%(email)s",
                 {'email': email})
    if len(user) == 0:
        return make_response("Wrong password or username", 401)
    user = user[0]

    if int(user['failed_login_count']) >= ATTEMPTS_BEFORE_COOLDOWN:
        if int((datetime.datetime.now() - user['failed_login_count']).total_seconds()) > COOLDOWN_TIME_SECONDS:
            query_update("UPDATE users SET failed_login_count = 0 where userid = %(userid)s",
                         {'userid': user['userid']})
        else:
            return make_response("Acces Denied, your account is blocked for " +
                                 str(int((datetime.datetime.now() - user[
                                     'last_failed_login']).total_seconds()) - ATTEMPTS_BEFORE_COOLDOWN) +
                                 " more seconds", 401)
    if not user['password_hash'] == send_password:
        query_update("UPDATE users SET last_failed_login = NOW(), failed_login_count = failed_login_count + 1 where "
                     "userid = %(userid)s", {'userid': user['userid']})
        return make_response("Wrong password or username", 401)
    access_token = create_access_token(identity=user['userid'])
    refresh_token = create_refresh_token(identity=user['userid'])

    resp = jsonify({'login': True})
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)
    return resp, 200


@jwt_required(refresh=True)
def refresh():
    # Create the new access token
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)

    # Set the access JWT and CSRF double submit protection cookies
    # in this response
    resp = jsonify({'refresh': True})
    set_access_cookies(resp, access_token)
    return resp, 200


# Because the JWTs are stored in an httponly cookie now, we cannot
# log the user out by simply deleting the cookie in the frontend.
# We need the backend to send us a response to delete the cookies
# in order to logout. unset_jwt_cookies is a helper function to
# do just that.
@jwt_required
def logout():
    resp = jsonify({'logout': True})
    unset_jwt_cookies(resp)
    return resp, 200
