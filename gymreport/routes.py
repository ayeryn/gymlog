from flask import render_template, flash, redirect, url_for, request, abort
# from gymreport.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from gymreport import app
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