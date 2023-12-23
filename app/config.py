import json

with open("/etc/gymlog_config.json") as config_file:
    config = json.load(config_file)

class Config(object):
    SECRET_KEY = config.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = config.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    print(f"================DB IS {SQLALCHEMY_DATABASE_URI}============")
    ADMINS = ["erynli@utexas.edu"]
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    # Whether to enable encrypted connections
    MAIL_USE_TLS = True
    MAIL_USERNAME = config.get("MAIL_USERNAME")
    MAIL_PASSWORD = config.get("MAIL_PASSWORD")
