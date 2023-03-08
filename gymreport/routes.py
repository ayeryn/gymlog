from flask import render_template, flash, redirect, url_for, request, abort
from gymreport.forms import ClassForm
from gymreport import app, db
from gymreport.models import GymClass

gym_classes = [
    {
        'name' : 'One & done',
        'class_type': 'HIIT'
    },
    {
        'name': 'Swimming',
        'class_type': 'Swimming'
    }
]

attendance_list = [
    {
         'author': 'user1',
         'title': 'Title',
         'content': 'Stuffs',
         'date_posted': 'March 11, 2022'
     },
     {
         'author': 'user2',
         'title': 'Today',
         'content': 'Things',
         'date_posted': 'May 1, 2000'
     }
]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/classes')
def classes():
    return render_template('classes.html', title='Classes', gym_classes=gym_classes)

@app.route('/new_class', methods=['GET', 'POST'])
def new_class():
    form = ClassForm()

    if form.validate_on_submit():
        c = GymClass(name=form.name.data, class_type=form.class_type.data)
        db.session.add(c)
        db.session.commit()
        return redirect(url_for('classes', title='Classes'))
    return render_template('add_class.html', legend='New Class', form=form)