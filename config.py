"""This module contains configs for the flask app."""
import os
import uuid

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """This class contains configs for the flask app."""

    SECRET_KEY = os.environ.get('SECRET_KEY', str(uuid.uuid1()))

    # Database config
    default_db = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', default_db)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'localhost')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 8025)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['your-email@example.com']
