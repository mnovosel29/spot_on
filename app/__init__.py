import os

from flask import Flask
from flask_babel import format_datetime

from app.routes.auth.forms import ExtendedRegisterForm
from config import Config
from app.extensions import db
from app.extensions import babel
from flask_migrate import Migrate
from flask_debugtoolbar import DebugToolbarExtension
from flask_mail import Mail
from flask_security import SQLAlchemySessionUserDatastore, Security
from app.models.auth import User, Role
from app.models.avatar import Avatar
from app.models.event import Event
from app.models.seat import Seat
from app.models.reservation import Reservation
from app.models.event_image import EventImage
from app.routes import (
    home_bp,
    auth_bp,
    dashboard_bp,
    users_bp,
    api_bp,
    event_bp,
    seat_bp
)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)
    migrate = Migrate(app, db)
    babel.init_app(app, default_locale=os.environ.get('DEFAULT_LANGUAGE'))
    toolbar = DebugToolbarExtension(app)
    mail = Mail(app)

    user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
    security = Security(app, user_datastore, confirm_register_form=ExtendedRegisterForm)

    @app.context_processor
    def inject_format_datetime():
        return {'format_datetime': format_datetime}

    # Register blueprints here
    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(event_bp, url_prefix='/events')
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(seat_bp, url_prefix='/seats')

    return app
