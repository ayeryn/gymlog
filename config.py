import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "85d7836bac21fafd3ed57a1d18c06518"

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "instance", "site.db")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ADMINS = ["erynli@utexas.edu"]

    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    # Whether to enable encrypted connections
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
