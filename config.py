import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or '85d7836bac21fafd3ed57a1d18c06518'

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') \
        or 'sqlite:///' + os.path.join(basedir, 'app.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
