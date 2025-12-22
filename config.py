import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    LISTEN = os.getenv('LISTEN_IP', default='0.0.0.0')
    LISTEN_PORT = os.getenv('LISTEN_PORT', default='80')
    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT')
    SCOPE = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    SCOPES = 'https://www.googleapis.com/auth/documents.readonly'
    DISCOVERY_DOC = 'https://docs.googleapis.com/$discovery/rest?version=v1'
    INCLUDE_LINK = os.getenv('INCLUDE_LINK', default=False)
    MAILLIST_GDOCS_ID=os.getenv('MAILLIST_GDOCS_ID')
    SERVER_NAME=os.getenv('SERVER_NAME', default='localhost')
    PREFERRED_URL_SCHEME = os.getenv('PREFERRED_URL_SCHEME', default='http')
    MAILLIST_JSON_KEYFILE = os.getenv('MAILLIST_JSON_KEYFILE', default='keyfile_do_listy_odbiorcow.json')
    MAILLIST_JSON_CREDENTIALS_FILE = os.getenv('MAILLIST_JSON_CREDENTIALS_FILE', default='credentialsfile_do_listy_odbiorcow.json')
    MAILGUN_API_BASE = os.getenv('MAILGUN_API_BASE', default="https://api.eu.mailgun.net/v3")
    MAILGUN_DOMAIN = os.getenv('MAILGUN_DOMAIN')
    MAILGUN_API_KEY = os.getenv('MAILGUN_API_KEY')
    DEPLOYMENT_NAME = 'prod'
    PYTHON_UNBUFFERED = os.getenv('PYTHON_UNBUFFERED', default=True)

class DevelopmentConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
    SERVER_NAME = 'localhost:5000'
    LISTEN = '127.0.0.1'
    LISTEN_PORT = 5000
    MAILLIST_GDOCS_ID=os.getenv('MAILLIST_GDOCS_ID')
    MAILLIST_JSON_KEYFILE = os.getenv('MAILLIST_JSON_KEYFILE', default='keyfile_do_listy_odbiorcow.json')
    MAILLIST_JSON_CREDENTIALS_FILE = os.getenv('MAILLIST_JSON_CREDENTIALS_FILE', default='credentialsfile_do_listy_odbiorcow.json')
    DEPLOYMENT_NAME = 'dev'
