from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"
mail = Mail(app)

from app.attendances.routes import attendances
from app.classes.routes import classes
from app.main.routes import main
from app.reports.routes import reports
from app.upload.routes import upload
from app.users.routes import users

app.register_blueprint(attendances)
app.register_blueprint(classes)
app.register_blueprint(main)
app.register_blueprint(reports)
app.register_blueprint(upload)
app.register_blueprint(users)
