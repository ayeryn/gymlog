from app import db
from datetime import date


class GymClass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    class_type = db.Column(db.String(3), default='Workout')
    attendance_list = db.relationship(
        'Attendance', backref='class_taken', lazy=True)

    def __repr__(self) -> str:
        return f'Class({self.name}, {self.class_type})'

    # Make object sortable by name
    def __lt__(self, other):
        return self.name < other.name


class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey(
        'gym_class.id'), nullable=False)
    date_attended = db.Column(db.Date, nullable=False,
                              default=date.today)

    def __repr__(self) -> str:
        date_formatted = self.date_attended.strftime("%Y-%m-%d")
        return f'Attendance({self.class_taken.name}, {date_formatted})'

    # Make object sortable by date
    def __lt__(self, other):
        return self.date_attended < other.date_attended
