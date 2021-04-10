import logging.config
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

from flask_bcrypt import Bcrypt


db = SQLAlchemy()
flask_bcrypt = Bcrypt()

def create_app(config_type='dev'):
    from config import config
    sentry_sdk.init(
        dsn="https://48176c69591e4580b6d69cedb4b09b62@sentry.io/3962456",
        integrations=[FlaskIntegration()]
    )
    app = Flask(__name__)
    logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../logging.conf'))
    app.config.from_object(config[config_type])
    SECRET_KEY = app.config["SECRET_KEY"]
    db.init_app(app)
    flask_bcrypt.init_app(app)
    logging.config.fileConfig(logging_conf_path)
    log = logging.getLogger(__name__)
    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/api/v1')

    

    return app