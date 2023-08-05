import flask.json.provider
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys
from .config import config

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_mode):
    app = Flask(__name__)
    app.json.sort_keys = False
    app.config["RESTX_MASK_SWAGGER"] = False
    app.config.from_object(config[config_mode])
    db.init_app(app)
    migrate.init_app(app, db)

    return app
