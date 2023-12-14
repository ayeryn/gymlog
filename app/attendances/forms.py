from flask_wtf import FlaskForm
from wtforms import SubmitField, DateField, SelectField
from wtforms.validators import DataRequired

# from app.models import Attendance


class AttendanceForm(FlaskForm):
    class_id = SelectField("Class", validate_choice=[DataRequired()], coerce=int)
    date_attended = DateField("Date", validators=[DataRequired()])
    submit = SubmitField("Submit")

    # TODO: validate dupes
