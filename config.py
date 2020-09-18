import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """Base configuration."""
    SECRET_KEY = 'changethis'
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SECRET_KEY = 'changethis'
    SECURITY_PASSWORD_SALT = 'changethis'
    SCOPE = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    SCOPES = 'https://www.googleapis.com/auth/documents.readonly'
    DISCOVERY_DOC = 'https://docs.googleapis.com/$discovery/rest?version=v1'
    INCLUDE_LINK = os.getenv('INCLUDE_LINK', default=False)
    GMAIL_AUTH_PORT = 57901
    GMAIL_AUTH_HOSTNAME = 'localhost'

class ProductionConfigLarpmailer(Config):
    DEVELOPMENT = False
    DEBUG = False
    SERVER_NAME = os.environ.get('SERVER_NAME')
    LISTEN = '0.0.0.0'
    LISTEN_PORT = 80
    MAILLIST_GDOCS_ID = os.getenv('MAILLIST_GDOCS_ID', default="changethis")
    MAILLIST_JSON_KEYFILE = os.getenv('MAILLIST_JSON_KEYFILE', default='keyfile_do_listy_odbiorcow.json')
    MAILLIST_JSON_CREDENTIALS_FILE = os.getenv('MAILLIST_JSON_CREDENTIALS_FILE',
                                               default='credentialsfile_do_listy_odbiorcow.json')
    GMAIL_JSON = 'klucz_do_gmaila.json'

class DevelopmentConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
    SERVER_NAME = 'localhost:5000'
    LISTEN = '127.0.0.1'
    LISTEN_PORT = 5000
    MAILLIST_GDOCS_ID=os.getenv('MAILLIST_GDOCS_ID', default="changethis")
    MAILLIST_JSON_KEYFILE = os.getenv('MAILLIST_JSON_KEYFILE', default='keyfile_do_listy_odbiorcow.json')
    MAILLIST_JSON_CREDENTIALS_FILE = os.getenv('MAILLIST_JSON_CREDENTIALS_FILE', default='credentialsfile_do_listy_odbiorcow.json')
    GMAIL_JSON = 'klucz_do_gmaila.json'
    DEPLOYMENT_NAME = 'dev'
