from flask import render_template, flash, redirect, url_for, request
from gymreport.forms import ClassForm, AttendanceForm
from gymreport import app, db
from gymreport.models import GymClass, Attendance
import os


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


"""
Class related endpoints
"""


@app.route('/classes')
def classes():
    gym_classes = GymClass.query.all()
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
    attendance_list = Attendance.query.all()
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


"""
CSV loader
"""
ALLOWED_EXTENTIONS = set(['.csv'])


def allowed_file(filename):
    _, f_ext = os.path.splitext(filename)
    # flash(f'ext = {f_ext}')
    return f_ext in ALLOWED_EXTENTIONS


@ app.route('/upload', methods=['GET', 'POST'])
def upload_csv():
    if request.method == 'POST':
        file = request.files['file']
        # flash(f'filename = {file.filename}')
        if file and allowed_file(file.filename):
            file_path = os.path.join(
                app.root_path, 'csv/', file.filename)
            # flash(f'File path = {file_path}')
            file.save(file_path)

        return redirect(url_for('classes'))

    return render_template('upload.html', title="Upload CSV")
