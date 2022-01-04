import connexion
import src.config as config
from .extensions import db, jwt
from src.endpoints.auth import JWT_SECRET
from flask import request, jsonify

from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended import unset_jwt_cookies

url = 'mariadb+mariadbconnector://root:admin@127.0.0.1:3306/innovatieplatform'


def create_app():
    app = connexion.App(__name__, specification_dir="../")
    # Read the API.yml file to configure the endpoints
    app.add_api("API.yml")
    app.app.config['BASE_URL'] = 'http://127.0.0.1:5000'

    app.app.config['JWT_SECRET_KEY'] = JWT_SECRET
    app.app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.app.config[
        'JWT_COOKIE_CSRF_PROTECT'] = True
    app.app.config['JWT_CSRF_CHECK_FORM'] = True
    app.app.config['JWT_COOKIE_SECURE'] = False  # TODO Change in production

    app.app.config['SQLALCHEMY_POOL_SIZE'] = 20
    app.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.app.config['SQLALCHEMY_DATABASE_URI'] = url
    db.init_app(app.app)

    with app.app.app_context():
        db.create_engine(url, {})
        jwt.init_app(app.app)
        return app
