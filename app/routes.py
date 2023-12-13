from flask import render_template, flash, redirect, url_for, request
from app.forms import ClassForm, AttendanceForm
from app import app, db
from app.models import GymClass, Attendance
import os
from io import TextIOWrapper
from datetime import date, timedelta
from calendar import HTMLCalendar
import csv
from re import search
import requests
import json


def get_quote():
    r = requests.get(
        "https://api.quotable.io/quotes/random?tags=motivational|failure")
    data = json.loads(r.content)
    quote_dict = data[0]
    return quote_dict['content'], quote_dict['author']


@app.route('/')
@app.route('/home')
def home():
    quote, author = get_quote()
    return render_template('home.html', quote=quote, author=author)


"""
Class related endpoints
"""


@app.route('/classes')
def classes():
    page = request.args.get('page', 1, type=int)
    gym_classes = GymClass.query.order_by(
        GymClass.name).paginate(page=page, per_page=9)
    return render_template('classes.html', title='Classes', gym_classes=gym_classes)


def capitalize_str(s):
    return " ".join([x.capitalize() for x in s.split()])


@app.route('/new_class', methods=['GET', 'POST'])
def new_class():
    form = ClassForm()

    if form.validate_on_submit():
        c = GymClass(name=capitalize_str(form.name.data),
                     class_type=capitalize_str(form.class_type.data))
        db.session.add(c)
        db.session.commit()
        flash('New class added!', 'success')
        return redirect(url_for('classes', title='Classes'))

    return render_template('add_class.html', legend='New Class', form=form)


@app.route('/class/<int:class_id>')
def show_class(class_id):
    c = GymClass.query.get(class_id)
    return render_template('class.html', legend=c.name, gymclass=c)


@app.route('/class/<int:class_id>/update', methods=['GET', 'POST'])
def edit_class(class_id):
    c = GymClass.query.get(class_id)
    form = ClassForm()

    if c and form.validate_on_submit():
        c.name = capitalize_str(form.name.data)
        c.class_type = form.class_type.data
        db.session.add(c)
        db.session.commit()
        flash('Class updated!', 'success')

    elif request.method == 'GET':
        form.name.data = c.name
        form.class_type.data = c.class_type
        return render_template('add_class.html', legend='Update class', form=form)

    return redirect(url_for('classes'))


@app.route('/class/<int:class_id>/delete', methods=['POST'])
def delete_class(class_id):
    c = GymClass.query.get(class_id)
    class_name = c.name

    db.session.delete(c)
    db.session.commit()
    flash(f'{class_name} has been deleted!', 'success')

    return redirect(url_for('classes'))


"""
Attendance related endpoints
"""


@app.route('/attendances')
def attendances():
    page = request.args.get('page', 1, type=int)
    attendance_list = Attendance.query.order_by(
        Attendance.date_attended.desc()).paginate(page=page, per_page=15)
    return render_template('attendances.html', title='Attendances', attendance_list=attendance_list)


@app.route('/new_attendance', methods=['GET', 'POST'])
def new_attendance():
    form = AttendanceForm()
    form.class_id.choices = [(c.id, c.name)
                             for c in GymClass.query.all()]

    if form.validate_on_submit():
        a = Attendance(class_id=form.class_id.data,
                       date_attended=form.date_attended.data)
        db.session.add(a)
        db.session.commit()
        flash(f'New attendance added for {a.class_taken.name}!', 'success')
        return redirect(url_for('show_class', class_id=a.class_id))

    return render_template('add_attendance.html', legend='New Attendance', form=form)


@app.route('/attendance/<int:attendance_id>/update', methods=['GET', 'POST'])
def edit_attendance(attendance_id):
    a = Attendance.query.get(attendance_id)
    form = AttendanceForm()

    if a and form.validate_on_submit():
        a.class_id = form.class_id.data
        a.date_attended = form.date_attended.data
        db.session.add(a)
        db.session.commit()
        flash('Attendance updated!', 'success')
    elif request.method == 'GET':
        form.class_id.data = a.class_taken.name
        form.date_attended.data = a.date_attended
        return render_template('add_attendance.html', legend='Update Attendance', form=form)

    return redirect(url_for('attendances'))


@app.route('/attendance/<int:attendance_id>/delete', methods=['POST'])
def delete_attendance(attendance_id):
    a = Attendance.query.get(attendance_id)
    db.session.delete(a)
    db.session.commit()
    flash(f'Attendance has been deleted!', 'success')

    return redirect(url_for('attendances'))


"""
CSV loader
"""
ALLOWED_EXTENTIONS = set(['.csv'])


def process_csv_row(data, filename):
    # Parse filename
    year = filename[:4]
    month = filename[4:]

    # Parse row
    day = data[0]
    class_name = capitalize_str(data[1])

    date_attended = date(int(year), int(month), int(day))
    return class_name, date_attended


@ app.route('/upload', methods=['GET', 'POST'])
def upload_csv():
    if request.method == 'POST':
        file = request.files['file']
        f_name, f_ext = os.path.splitext(file.filename)

        if file and f_ext in ALLOWED_EXTENTIONS:
            file = TextIOWrapper(file, encoding='utf-8')
            csv_reader = csv.reader(file, delimiter=',')
            for row in csv_reader:
                class_name, date = process_csv_row(row, f_name)

                # Add GymClass if class doesn't exists
                c = GymClass.query.filter_by(name=class_name).first()
                if not c:
                    c = GymClass(name=class_name)
                    db.session.add(c)
                    db.session.commit()
                    flash(f'Class {class_name} created from csv', 'success')

                a = Attendance(class_id=c.id, date_attended=date)
                db.session.add(a)
                db.session.commit()
                flash(f'New attendance create for {class_name}', 'success')

        return redirect(url_for('classes'))

    return render_template('upload.html', title="Upload CSV")


"""
Reporting
"""


@app.route("/monthly_report")
def monthly_report():
    # TODO: Upload some mock data for current month
    # TODO: Query data for the report
    # TODO: able to grab current month's datas
    data = []
    for i in range(10):
        data.append((f'class_0{i}', i % 3 + 5))

    labels = [row[0] for row in data]
    values = [row[1] for row in data]
    return render_template('monthly_report.html', labels=labels, values=values)
