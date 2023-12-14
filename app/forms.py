from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    DateField,
    SelectField,
    PasswordField,
    BooleanField,
)
from wtforms.validators import DataRequired, Length, ValidationError, Email, EqualTo
from app.models import GymClass, Attendance, User


class ClassForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=3, max=20)])
    class_type = StringField("Type")
    submit = SubmitField("Submit")

    def validate_name(self, name):
        c = GymClass.query.filter_by(name=name.data).first()

        if c:
            raise ValidationError("Class exists!")


class AttendanceForm(FlaskForm):
    class_id = SelectField("Class", validate_choice=[DataRequired()], coerce=int)
    date_attended = DateField("Date", validators=[DataRequired()])
    submit = SubmitField("Submit")


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username exists. Please try again.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email exists. Please try again.")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")
