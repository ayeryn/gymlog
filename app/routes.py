from flask import render_template, flash, redirect, url_for, request
from app.forms import ClassForm, AttendanceForm, RegistrationForm, LoginForm
from app import app, db, bcrypt
from app.models import GymClass, Attendance, User
import os
from io import TextIOWrapper
from datetime import date
import csv
import requests
import json
from sqlalchemy import extract
from collections import defaultdict
from flask_login import login_user, current_user, logout_user, login_required


def get_quote():
    r = requests.get("https://api.quotable.io/quotes/random?tags=motivational|failure")
    data = json.loads(r.content)
    quote_dict = data[0]
    return quote_dict["content"], quote_dict["author"]


@app.route("/")
@app.route("/home")
def home():
    quote, author = get_quote()
    return render_template("home.html", quote=quote, author=author)


"""
Class related endpoints
"""


@app.route("/classes")
def classes():
    page = request.args.get("page", 1, type=int)
    gym_classes = GymClass.query.order_by(GymClass.name).paginate(page=page, per_page=9)
    return render_template("classes.html", title="Classes", gym_classes=gym_classes)


def capitalize_str(s):
    # Helper Function
    return ' '.join([x.capitalize() for x in s.split()])


@app.route("/new_class", methods=["GET", "POST"])
def new_class():
    form = ClassForm()

    if form.validate_on_submit():
        c = GymClass(
            name=capitalize_str(form.name.data),
            class_type=capitalize_str(form.class_type.data),
        )
        db.session.add(c)
        db.session.commit()
        flash("New class added!", "success")
        return redirect(url_for("classes", title="Classes"))

    return render_template("add_class.html", legend="New Class", form=form)


@app.route("/class/<int:class_id>")
def show_class(class_id):
    c = GymClass.query.get(class_id)
    return render_template("class.html", legend=c.name, gymclass=c)


@app.route("/class/<int:class_id>/update", methods=["GET", "POST"])
def edit_class(class_id):
    c = GymClass.query.get(class_id)
    form = ClassForm()

    if act and form.validate_on_submit():
        act.name = capitalize_str(form.name.data)
        db.session.add(act)
        db.session.commit()
        flash("Class updated!", "success")

    elif request.method == "GET":
        form.name.data = c.name
        form.class_type.data = c.class_type
        return render_template("add_class.html", legend="Update class", form=form)

    return redirect(url_for("classes"))


@app.route("/class/<int:class_id>/delete", methods=["POST"])
def delete_class(class_id):
    c = GymClass.query.get(class_id)
    class_name = c.name

    db.session.delete(act)
    db.session.commit()
    flash(f"{class_name} has been deleted!", "success")

    return redirect(url_for("classes"))


'''
Attendance related endpoints



@app.route("/attendances")
def attendances():
    page = request.args.get("page", 1, type=int)
    attendance_list = Attendance.query.order_by(
        Attendance.date_attended.desc()
    ).paginate(page=page, per_page=15)
    return render_template(
        "attendances.html", title="Attendances", attendance_list=attendance_list
    )


@app.route("/new_attendance", methods=["GET", "POST"])
def new_attendance():
    form = AttendanceForm()
    form.class_id.choices = [(c.id, c.name) for c in GymClass.query.all()]

    if form.validate_on_submit():
        a = Attendance(
            class_id=form.class_id.data, date_attended=form.date_attended.data
        )
        db.session.add(a)
        db.session.commit()
        flash(f"New attendance added for {a.class_taken.name}!", "success")
        return redirect(url_for("show_class", class_id=a.class_id))

    return render_template("add_attendance.html", legend="New Attendance", form=form)


@app.route("/attendance/<int:attendance_id>/update", methods=["GET", "POST"])
def edit_attendance(attendance_id):
    a = Attendance.query.get(attendance_id)
    form = AttendanceForm()

    if a and form.validate_on_submit():
        a.class_id = form.class_id.data
        a.date_attended = form.date_attended.data
        db.session.add(a)
        db.session.commit()
        flash("Attendance updated!", "success")
    elif request.method == "GET":
        form.class_id.data = a.class_taken.name
        form.date_attended.data = a.date_attended
        return render_template(
            "add_attendance.html", legend="Update Attendance", form=form
        )

    return redirect(url_for("attendances"))


@app.route("/attendance/<int:attendance_id>/delete", methods=["POST"])
def delete_attendance(attendance_id):
    a = Attendance.query.get(attendance_id)
    db.session.delete(a)
    db.session.commit()
    flash(f"Attendance has been deleted!", "success")

    return redirect(url_for("attendances"))

'''
CSV loader
"""
ALLOWED_EXTENTIONS = set([".csv"])


def process_csv_row(data, filename):
    # Parse filename
    year = filename[:4]
    month = filename[4:]

    # Parse row
    day = data[0]
    class_name = capitalize_str(data[1])

    date_attended = date(int(year), int(month), int(day))
    return class_name, date_attended


@app.route("/upload", methods=["GET", "POST"])
def upload_csv():
    if request.method == "POST":
        file = request.files["file"]
        f_name, f_ext = os.path.splitext(file.filename)

        if file and f_ext in ALLOWED_EXTENTIONS:
            file = TextIOWrapper(file, encoding="utf-8")
            csv_reader = csv.reader(file, delimiter=",")
            for row in csv_reader:
                class_name, date = process_csv_row(row, f_name)

                # Add Activity if class doesn't exists
                c = Activity.query.filter_by(name=class_name).first()
                if not c:
                    c = Activity(name=class_name)
                    db.session.add(c)
                    db.session.commit()
                    flash(f"Class {class_name} created from csv", "success")

                a = Attendance(class_id=c.id, date_attended=date)
                db.session.add(a)
                db.session.commit()
                flash(f"New attendance create for {class_name}", "success")

        return redirect(url_for("classes"))

    return render_template("upload.html", title="Upload CSV")


"""
Reporting
"""


@app.route("/monthly_report")
def monthly_report():
    today = date.today()
    attendances = Attendance.query.filter(
        extract("year", Attendance.date_attended) == today.year
    ).filter(extract("month", Attendance.date_attended) == today.month)

    data = defaultdict(int)
    for attendance in attendances:
        data[attendance.class_taken.name] += 1

    labels = [k for k in data.keys()]
    values = [v for v in data.values()]

    return render_template("monthly_report.html", labels=labels, values=values)


@app.route("/yearly_report")
def yearly_report():
    attendances = Attendance.query.filter(
        extract("year", Attendance.date_attended) == date.today().year
    )

    data = defaultdict(int)
    for attendance in attendances:
        data[attendance.class_taken.name] += 1

    labels = [k for k in data.keys()]
    values = [v for v in data.values()]

    return render_template("yearly_report.html", labels=labels, values=values)


"""
TODO:
- add profile pic page
- reset pw
"""


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("classes"))

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
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            if next_page:
                return redirect(next_page)
            return redirect(url_for("classes"))
        else:
            flash(f"Something went wrong :( Please check email and password.", "danger")
    return render_template("login.html", title="Login", form=form)


@app.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/account")
@login_required
def account():
    return render_template("account.html", title="My Account")
