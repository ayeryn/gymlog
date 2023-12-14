from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_user, current_user, logout_user, login_required
from app.users.forms import RegistrationForm, LoginForm
from app import db, bcrypt
from app.models import User


users = Blueprint("users", __name__)

"""
TODO:
- add profile pic page
- reset pw
"""


@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("classes.show_classes"))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(
            username=form.username.data, email=form.email.data, password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash(f"Your account has been created! Let's get you started :) ", "success")
        return redirect(url_for("classes.login"))
    return render_template("register.html", title="Register", form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            if next_page:
                return redirect(next_page)
            return redirect(url_for("classes.show_classes"))
        else:
            flash(f"Something went wrong :( Please check email and password.", "danger")
    return render_template("login.html", title="Login", form=form)


@users.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for("main.home"))


@users.route("/account")
@login_required
def account():
    return render_template("account.html", title="My Account")