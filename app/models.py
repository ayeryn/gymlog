from datetime import datetime
from flask_login import UserMixin
from app import db, bcrypt, login


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    avatar_file = db.Column(
        db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60))
    attendances = db.Relationship('Attendance', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.avatar_file}')"

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(
            password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)


class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), unique=True, nullable=False)
    category = db.Column(db.String(15), nullable=False)
    attendances = db.Relationship('Attendance', backref='activity', lazy=True)

    def __repr__(self):
        return f"Activity('{self.name}', '{self.category}')"

        # Make object sortable by name
    def __lt__(self, other):
        return self.name < other.name


class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.Integer, db.ForeignKey(
        'activity.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False)
    date_attended = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        # TODO:
        # Add act name and user name
        return f"Attendance('{self.date_attended}')"
