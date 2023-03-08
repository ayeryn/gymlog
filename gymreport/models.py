from gymreport import db
from datetime import datetime


class GymClass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    class_type = db.Column(db.String(10), default='Workout')
    attendance_list = db.relationship(
        'Attendance', backref='class_taken', lazy=True)

    def __repr__(self) -> str:
        return f'Class(name={self.name}, type={self.class_type})'


class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey(
        'gym_class.id'), nullable=False)
    date_attended = db.Column(db.DateTime, nullable=False,
                              default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'Attendance(class={self.class_taken.name}, date_attended={self.date_attended}'
