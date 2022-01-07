import connexion
import src.config as config
from .extensions import db, jwt
import src.config as config
from flask import request, jsonify

from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended import unset_jwt_cookies


def create_app():
    app = connexion.App(__name__, specification_dir="../")
    # Read the API.yml file to configure the endpoints
    app.add_api("API.yml")
    app.app.config['BASE_URL'] = 'http://127.0.0.1:5000'

    app.app.config['JWT_ENCODE_ISSUER'] = config.JWT_ISSUER
    app.app.config['JWT_DECODE_ISSUER'] = config.JWT_ISSUER
    app.app.config['JWT_ALGORITHM'] = config.JWT_ALGORITHM
    app.app.config['JWT_ACCESS_TOKEN_EXPIRES'] = config.JWT_LIFETIME_SECONDS
    app.app.config['JWT_SECRET_KEY'] = config.JWT_SECRET
    app.app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.app.config['JWT_COOKIE_CSRF_PROTECT'] = True
    app.app.config['JWT_CSRF_CHECK_FORM'] = True
    app.app.config['JWT_COOKIE_SECURE'] = False  # TODO Change in production

    app.app.config['SQLALCHEMY_POOL_SIZE'] = 20
    app.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URL
    db.init_app(app.app)

    with app.app.app_context():
        db.create_engine(config.DATABASE_URL, {})
        jwt.init_app(app.app)
        return app
