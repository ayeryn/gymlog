from datetime import datetime
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    avatar_file = db.Column(
        db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    attendances = db.Relationship('Attendance', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.avatar_file}')"


class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), unique=True, nullable=False)
    category = db.Column(db.String(15), unique=True, nullable=False)
    attendances = db.Relationship('Attendance', backref='activity', lazy=True)

    def __repr__(self):
        return f"Activity('{self.name}', '{self.category}')"


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
