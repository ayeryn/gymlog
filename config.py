import os


class Config(object):

    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or "85d7836bac21fafd3ed57a1d18c06518"

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'SQLALCHEMY_DATABASE_URI') or "sqlite:///site.db"
