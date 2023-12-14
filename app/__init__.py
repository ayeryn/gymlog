from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# from flask_mail import Mail

# import logging
# from logging.handlers import SMTPHandler


app = Flask(__name__)
app.config.from_object(Config)


db = SQLAlchemy(app)
migrate = Migrate(app, db, compare_type=True)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

# mail = Mail(app)

from app import routes

# from app import routes, models

# Only send logs to email when the app is running without debug mode
# if not app.debug:
#     if app.config["MAIL_SERVER"]:
#         auth = None
#         if app.config["MAIL_USERNAME"] or app.config["MAIL_PASSWORD"]:
#             auth = (app.config["MAIL_USERNAME"], app.config["MAIL_PASSWORD"])
#         secure = None
#         if app.config["MAIL_USE_TLS"]:
#             secure = ()
#         mail_handler = SMTPHandler(
#             mailhost=(app.config["MAIL_SERVER"], app.config["MAIL_PORT"]),
#             fromaddr="no-reply@" + app.config["MAIL_SERVER"],
#             toaddrs=app.config["ADMINS"],
#             subject="Gymlog Failure",
#             credentials=auth,
#             secure=secure,
#         )

# Only report errors
# and not warning/debugging msgs/etc.
# mail_handler.setLevel(logging.ERROR)

# Attach handler to the Flask logger
# app.logger.addHandler(mail_handler)
