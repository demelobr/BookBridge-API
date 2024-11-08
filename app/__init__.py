from flask import Flask
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

from .resources.users import users_blueprint
from .resources.clubs import clubs_blueprint
from sql_alchemy import db

import os

def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
    app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY')

    db.init_app(app)
    jwt = JWTManager(app)

    app.register_blueprint(users_blueprint)
    app.register_blueprint(clubs_blueprint)

    return app