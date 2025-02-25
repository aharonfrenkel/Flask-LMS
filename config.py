import os

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from dotenv import load_dotenv
from datetime import timedelta


load_dotenv()


class Config:
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

    # Mail Settings
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')

    # APISpec
    APISPEC_SPEC = APISpec(
        title='LMS API',
        version='1.0.0',
        openapi_version='3.0.2',
        plugins=[FlaskPlugin(), MarshmallowPlugin()],
        info={
            'description': 'API endpoints for Learning Management System'
        }
    )
    APISPEC_SWAGGER_URL = '/swagger/'
    APISPEC_SWAGGER_UI_URL = '/swagger-ui/'