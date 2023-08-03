from flask import render_template, url_for, flash, redirect
from app import app, db, bcrypt
from app.models import User, Activity, Attendance
from app.forms import RegistrationForm, LoginForm


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
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created! You are now able to log in.", "success")
        return redirect(url_for('login'))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'e@test.com' and form.password.data == "pwd":
            flash(f"You have been logged in!", "success")
            return redirect(url_for("home"))
        else:
            flash(f"Login unsuccessful! Please check username and password", "danger")
    return render_template("login.html", title="Login", form=form)
