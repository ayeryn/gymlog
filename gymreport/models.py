from gymreport import db
from datetime import datetime

class GymClass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    class_type = db.Column(db.String(20))

    def __repr__(self) -> str:
        return f"Class('{self.name}', '{self.type}')"
    
class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)
    date_attended = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"Attendance('{self.class_id}', '{self.date_attended}')"