import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or '85d7836bac21fafd3ed57a1d18c06518'

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') \
        or 'sqlite:///' + os.path.join(basedir, 'app.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    # Whether to enable encrypted connections
    MAIL_USE_TLS = os.environ.get('MAIL_USER_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['erynli@utexas.edu']
