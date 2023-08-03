from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import RegistrationForm, LoginForm
from flask_migrate import Migrate

app = Flask(__name__)

# Python module secrets
app.config["SECRET_KEY"] = "85d7836bac21fafd3ed57a1d18c06518"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    avatar_file = db.Column(
        db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    attendances = db.Relationship('Attendance', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.id}', '{self.username}', '{self.email}', '{self.avatar_file}')"


class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), unique=True, nullable=False)
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
        return f"Attendance('{self.activity_id}', '{self.user_id}',{self.date_attended}')"


@app.route("/")
@app.route("/home")
def home():
    activities = Activity.query.all()
    return render_template("home.html", activities=activities)


@app.route("/about")
def about():
    return render_template("about.html", title='About')


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for("home"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'test@a.com' and form.password.data == "12345":
            flash(f"You have been logged in!", "success")
            return redirect(url_for("home"))
        else:
            flash(f"Login unsuccessful! Please check username and password", "danger")
    return render_template("login.html", title="Login", form=form)


if __name__ == "__main__":
    app.run(debug=True)
