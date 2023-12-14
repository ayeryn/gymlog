from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from app.models import GymClass


class ClassForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=3, max=20)])
    class_type = StringField("Type")
    submit = SubmitField("Submit")

    def validate_name(self, name):
        c = GymClass.query.filter_by(name=name.data).first()

        if c:
            raise ValidationError("Class exists!")
