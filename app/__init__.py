from flask import Flask
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

from .resources.users import users_blueprint
from .resources.clubs import clubs_blueprint
from .resources.books import books_blueprint
from .resources.reviews import review_blueprint
from sql_alchemy import db

import os

def create_app(config_name=None):
    load_dotenv()

    app = Flask(__name__)
    if config_name == 'testing': 
        app.config.from_object('config.TestingConfig') 
    else: 
        app.config.from_object('config.DevelopmentConfig')        

    db.init_app(app)
    jwt = JWTManager(app)

    app.register_blueprint(users_blueprint)
    app.register_blueprint(clubs_blueprint)
    app.register_blueprint(books_blueprint)
    app.register_blueprint(review_blueprint)

    return app