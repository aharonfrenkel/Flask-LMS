from flask import Flask

from config import Config
from app.extensions import db, ma, login_manager, mail


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    ma.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from app.routes import auth_bp

    app.register_blueprint(auth_bp)

    @login_manager.user_loader
    def user_loader(user_id):
        from app.models import User
        return User.query.get(int(user_id))

    return app