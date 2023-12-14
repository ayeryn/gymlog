from app import db, login_manager
from datetime import date
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    avatar_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User({self.username}, {self.email}, {self.avatar_file})"


class GymClass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    class_type = db.Column(db.String(3), default="Workout")
    attendance_list = db.relationship("Attendance", backref="class_taken", lazy=True)

    def __repr__(self) -> str:
        return f"Class({self.name}, {self.class_type})"

    # Make object sortable by name
    def __lt__(self, other):
        return self.name < other.name


class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey("gym_class.id"), nullable=False)
    date_attended = db.Column(db.Date, nullable=False, default=date.today)

    def __repr__(self) -> str:
        date_formatted = self.date_attended.strftime("%Y-%m-%d")
        return f"Attendance({self.class_taken.name}, {date_formatted})"

    # Make object sortable by date
    def __lt__(self, other):
        return self.date_attended < other.date_attended
