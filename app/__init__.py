from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from app.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from app.attendances.routes import attendances
    from app.classes.routes import classes
    from app.main.routes import main
    from app.reports.routes import reports
    from app.upload.routes import upload
    from app.users.routes import users
    from app.errors.handlers import errors

    app.register_blueprint(attendances)
    app.register_blueprint(classes)
    app.register_blueprint(main)
    app.register_blueprint(reports)
    app.register_blueprint(upload)
    app.register_blueprint(users)
    app.register_blueprint(errors)

    return app
