# project/config.py

import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """Base configuration."""
    SECRET_KEY = 'ohjich4icheicheijoH6Aniequooca    '
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SECRET_KEY = 'Ohquai7ia8ogeingie1ooGh6reer8v'
    SECURITY_PASSWORD_SALT = 'ao0cav8ooSeim3Naey0aive4gaiDie'
    SCOPE = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    SCOPES = 'https://www.googleapis.com/auth/documents.readonly'
    DISCOVERY_DOC = 'https://docs.googleapis.com/$discovery/rest?version=v1'
    INCLUDE_LINK = os.getenv('INCLUDE_LINK', default=False)

class ProductionConfigLarpmailer(Config):
    DEVELOPMENT = False
    DEBUG = False
    SERVER_NAME = os.environ.get('SERVER_NAME')
    LISTEN = '0.0.0.0'
    LISTEN_PORT = 80
    MAILLIST_GDOCS_ID = os.getenv('MAILLIST_GDOCS_ID', default="1h3mXQ3sm0XBw_QzKkz6NLEuOeLzCJncJ66JXYDO-Kkk")
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
    MAILLIST_GDOCS_ID=os.getenv('MAILLIST_GDOCS_ID', default="1h3mXQ3sm0XBw_QzKkz6NLEuOeLzCJncJ66JXYDO-Kkk")
    MAILLIST_JSON_KEYFILE = os.getenv('MAILLIST_JSON_KEYFILE', default='keyfile_do_listy_odbiorcow.json')
    MAILLIST_JSON_CREDENTIALS_FILE = os.getenv('MAILLIST_JSON_CREDENTIALS_FILE', default='credentialsfile_do_listy_odbiorcow.json')
    GMAIL_JSON = 'klucz_do_gmaila.json'
    DEPLOYMENT_NAME = 'larpmailerdev'
