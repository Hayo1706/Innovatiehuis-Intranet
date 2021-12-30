import connexion
import flask
from flask_cors import CORS
from flask_jwt_extended import jwt_required
from sqlalchemy import create_engine

from .extensions import db, jwt
from .JWT import JWT_SECRET
from flask import request

from flask_jwt_extended import verify_jwt_in_request

url = 'mariadb+mariadbconnector://root:admin@127.0.0.1:3306/innovatieplatform'


def create_app():
    app = connexion.App(__name__, specification_dir="../")
    # Read the API.yml file to configure the endpoints
    app.add_api("API.yml")
    app.app.config['BASE_URL'] = 'http://127.0.0.1:5000'

    app.app.config['JWT_SECRET_KEY'] = JWT_SECRET
    app.app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.app.config[
        'JWT_COOKIE_CSRF_PROTECT'] = True  # TODO Regel dit, csrf token moet meegestuurd worden in frontend
    app.app.config['JWT_CSRF_CHECK_FORM'] = True  # TODO Regel dit ook

    app.app.config['SQLALCHEMY_POOL_SIZE'] = 20
    app.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.app.config['SQLALCHEMY_DATABASE_URI'] = url
    db.init_app(app.app)

    @app.app.before_request
    def hoi():
        if not request.base_url == 'http://127.0.0.1:5000/api/auth':
            # verify_jwt_in_request()
            print()

    with app.app.app_context():
        db.create_engine(url, {})
        jwt.init_app(app.app)
        return app
