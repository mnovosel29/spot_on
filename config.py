import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG')

    SECRET_KEY = os.environ.get('SECRET_KEY')
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT')
    SECURITY_REGISTERABLE = os.environ.get('SECURITY_REGISTERABLE')
    SECURITY_CONFIRMABLE = os.environ.get('SECURITY_CONFIRMABLE')
    SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS = True
    SECURITY_POST_REGISTER_VIEW = os.environ.get('SECURITY_POST_REGISTER_VIEW') or 'security.login'
    SECURITY_POST_LOGIN_VIEW = os.environ.get('SECURITY_POST_LOGIN_VIEW') or 'home.index'
    SECURITY_RECOVERABLE = os.environ.get('SECURITY_RECOVERABLE', True)
    SECURITY_I18N_DIRNAME = ["builtin", "app/translations"]
    SECURITY_UNAUTHORIZED_VIEW = os.environ.get('SECURITY_UNAUTHORIZED_VIEW') or 'security.login'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')\
        or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    SQLALCHEMY_RECORD_QUERIES = os.environ.get('SQLALCHEMY_RECORD_QUERIES')

    LANGUAGES = os.getenv('LANGUAGES').split(',')
    DEFAULT_LANGUAGE = os.getenv('DEFAULT_LANGUAGE')

    DEBUG_TB_INTERCEPT_REDIRECTS = False

    # Flask-Mail configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS')

    # Flask-Security translations
    SECURITY_MSG_USER_DOES_NOT_EXIST = ('Invalid email or password!', 'error')
    SECURITY_MSG_INVALID_PASSWORD = ('Invalid email or password!', 'error')
    SECURITY_MSG_CONFIRMATION_REQUIRED = ('Email is not confirmed, please confirm Email.', 'error')
    SECURITY_MSG_EMAIL_CONFIRMED = ('Thank you. Email is confirmed.', 'info')
    SECURITY_MSG_ALREADY_CONFIRMED = ('Email is already confirmed.', 'info')
    SECURITY_MSG_INVALID_CONFIRMATION_TOKEN = ('Invalid confirmation token.', 'error')
    SECURITY_MSG_DISABLED_ACCOUNT = ('Account is disabled.', 'error')
    SECURITY_MSG_LOGIN_EMAIL_SENT = ('Instructions to reset your password have been sent', 'info')
    SECURITY_MSG_PASSWORD_RESET_REQUEST = ('Instructions to reset your password have been sent', 'info')
    SECURITY_MSG_CONFIRM_REGISTRATION = ('Thank you. Confirmation instructions have been sent to your email', 'info')
    SECURITY_MSG_PASSWORD_RESET_NO_LOGIN = ('You successfully reset your password. Please login.', 'success')
    SECURITY_MSG_UNAUTHORIZED = ('You do not have permission to view this resource.', 'error')
    SECURITY_MSG_UNAUTHENTICATED = ('You must be logged in to view this resource.', 'error')
