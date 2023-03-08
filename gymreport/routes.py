from flask import render_template, flash, redirect, url_for, request, abort
# from gymreport.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from gymreport import app
# from gymreport.models import Class, Month


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')
