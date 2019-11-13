import os
import uuid
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))
# Default database config
default_db = 'sqlite:///' + os.path.join(basedir, 'app.db')

class Config(object):
    """This class contains configs for the flask app."""

    SECRET_KEY = os.environ.get('SECRET_KEY', "sitesecretkey")
    # Database config
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', default_db)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'localhost')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 8025)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['no-reply@yahoo.com']
    POSTS_PER_PAGE = 25
    LANGUAGES = ['en', 'es']
    MS_TRANSLATOR_KEY = os.environ.get("MS_TRANSLATOR_KEY", "05173a07bd024685b5d70e0849bbbb47")
    # MS_TRANSLATOR_KEY="05173a07bd024685b5d70e0849bbbb47"
    # MS_TRANSLATOR_ENDPOINT="https://translator101.cognitiveservices.azure.com/sts/v1.0/issuetoken"
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL', r"http://localhost:9200")
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
