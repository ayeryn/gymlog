from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from gymreport.models import GymClass

class ClassForm(FlaskForm):
    name = StringField('name', validators=[DataRequired(), Length(min=3, max=20)])
    class_type = StringField('type')
    submit = SubmitField('Submit')

