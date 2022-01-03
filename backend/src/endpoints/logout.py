from flask import jsonify

from flask_jwt_extended import unset_jwt_cookies

# Because the JWTs are stored in an httponly cookie now, we cannot
# log the user out by simply deleting the cookie in the frontend.
# We need the backend to send us a response to delete the cookies
# in order to logout. unset_jwt_cookies is a helper function to
# do just that.

def logout():
    resp = jsonify({'logout': True})
    unset_jwt_cookies(resp)
    return resp, 200