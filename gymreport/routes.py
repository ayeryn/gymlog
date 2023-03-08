from flask import render_template, flash, redirect, url_for, request
from gymreport.forms import ClassForm
from gymreport import app, db
from gymreport.models import GymClass

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
    gym_classes = GymClass.query.all()
    return render_template('classes.html', title='Classes', gym_classes=gym_classes)

def capitalize_str(s):
    return " ".join([x.capitalize() for x in s.split()])

@app.route('/new_class', methods=['GET', 'POST'])
def new_class():
    form = ClassForm()

    if form.validate_on_submit():
        c = GymClass(name=capitalize_str(form.name.data), class_type=form.class_type.data)
        db.session.add(c)
        db.session.commit()
        flash('New class added!', 'success')
        return redirect(url_for('classes', title='Classes'))
    

    return render_template('add_class.html', legend='New Class', form=form)

@app.route('/class/<int:class_id>', methods=['GET', 'POST'])
def edit_class(class_id):
    c = GymClass.query.get(class_id)

    form = ClassForm()

    if c and form.validate_on_submit():
        c.name=capitalize_str(form.name.data)
        c.class_type=form.class_type.data
        db.session.add(c)
        db.session.commit()
        flash('Class updated!', 'success')
    elif request.method == 'GET':
        form.name.data = c.name
        form.class_type.data = c.class_type
        return render_template('add_class.html', legend='Update class', form=form)
    
    return redirect(url_for('classes'))