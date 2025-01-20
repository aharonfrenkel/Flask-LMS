from flask import Flask

from config import Config
from app.extensions import db, ma, bcrypt, login_manager, mail


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    return app