from flask import render_template, flash, redirect, url_for, request
from gymreport.forms import ClassForm, AttendanceForm
from gymreport import app, db
from gymreport.models import GymClass, Attendance

attendance_list = [
    {
        'class_taken': 1,
        'date_attended': '20230109'
    },
    {
        'class_taken': 3,
        'date_attended': '20230309'
    }
]


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


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
        c = ClassForm(name=capitalize_str(
            form.name.data), class_type=form.class_type.data)
        db.session.add(c)
        db.session.commit()
        flash('New class added!', 'success')
        return redirect(url_for('classes', title='Classes'))

    return render_template('add_class.html', legend='New Class', form=form)


@app.route('/class/<int:class_id>')
def show_class(class_id):
    c = GymClass.query.get(class_id)
    # attendance_list = Attendance.query.filter_by(class_taken=class_id)

    return render_template('class.html', legend=c.name, gymclass=c)
    # return render_template('class.html', legend17=c.name, gymclass=c, attendance_list=attendance_list)


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


@ app.route('/attendances')
def attendances():
    # gym_classes = GymClass.query.all()
    return render_template('attendances.html', title='Attendances', attendance_list=attendance_list)


@ app.route('/new_class', methods=['GET', 'POST'])
def new_attendance():
    form = AttendanceForm()
    form.class_taken.choices = [(c.id, c.name)
                                for c in GymClass.query.all()]

    if form.validate_on_submit():
        a = Attendance(class_taken=form.name.data,
                       date_attended=form.date_attended.data)
        db.session.add(a)
        db.session.commit()
        flash(f'New attendance added for {form.name.data}!', 'success')
        return redirect(url_for('classes', title='Classes'))

    return render_template('add_class.html', legend='New Class', form=form)

# @app.route('/class/<int:class_id>', methods=['GET', 'POST'])
# def edit_class(class_id):
#     c = GymClass.query.get(class_id)

#     form = ClassForm()

#     if c and form.validate_on_submit():
#         c.name=capitalize_str(form.name.data)
#         c.class_type=form.class_type.data
#         db.session.add(c)
#         db.session.commit()
#         flash('Class updated!', 'success')
#     elif request.method == 'GET':
#         form.name.data = c.name
#         form.class_type.data = c.class_type
#         return render_template('add_class.html', legend='Update class', form=form)

#     return redirect(url_for('classes'))
