import secrets
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


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'You have been logged in!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        flash('Invalid email or password')
        return redirect(url_for('login'))
    return render_template('login.html', title='Login', form=form)


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for instructions to reset your password')
        return redirect(url_for('login'))
    return render_template(
        'reset_password_request.html',
        title='Reset Password Request',
        form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    user = User.verify_reset_password_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_password_request'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset!')
        return redirect(url_for('login'))

    return render_template('reset_password.html', title='Reset Password', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    '''
    Return picture_fn (string)

    1. picture_fn - generates a randomized filename by concatenating a random hex, 
    and the extension of the picture being uploaded
    2. picture_path - generates the abs path of where to upload the file to
    3. resizes picture
    4. saves file at picture_path
    '''
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)
    return picture_fn


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.avatar_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()

        flash('You account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for(
        'static', filename='profile_pics/' + current_user.avatar_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


'''
DEV branches
'''

# def format_day(html, day, style_class='cal-text-attend'):
#     pat = f'class='[a-z]+'>{day.day}<'
#     s_ind, e_ind = search(pat, html).span()
#     weekday = day.strftime('%a').lower()
#     if day == date.today():
#         rs = f'class='{weekday} {style_class} cal-today'>{day.day}<'
#     else:
#         rs = f'class='{weekday} {style_class}'>{day.day}<'

#     return html.replace(html[s_ind:e_ind], rs)


# def format_month():
#     '''
#     Add styling on top of HTMLCalendar format
#     - add cal-today to today's class
#     - add cal-text to the rest of the month
#     '''
#     now = date.today()
#     cal = HTMLCalendar()
#     cal_html = cal.formatmonth(theyear=now.year, themonth=now.month)

#     # Format days with workouts
#     curr_month_start = now.replace(day=1)
#     next_month_start = (curr_month_start + timedelta(days=32)).replace(day=1)
#     days_attended = db.session.query(Attendance).filter(
#         Attendance.date_attended >= curr_month_start, Attendance.date_attended < next_month_start)

#     for d in days_attended:
#         print(f'd.date_attended = {d.date_attended}')
#         cal_html = format_day(cal_html, d.date_attended)

#     return cal_html


'''
Activity related endpoints
'''


@app.route('/activities')
def activities():
    page = request.args.get('page', 1, type=int)
    activities = Activity.query.order_by(
        Activity.name).paginate(page=page, per_page=9)
    return render_template('activities.html', title='Activities', activities=activities)


def capitalize_str(s):
    # Helper Function
    return ' '.join([x.capitalize() for x in s.split()])


# @app.route('/activity/<int:activity_id>')
# def activity(activity_id):
#     a = Activity.query.get(activity_id)
#     return render_template('activity.html', legend=a.name, activity=a)


@app.route('/new_activity', methods=['GET', 'POST'])
@login_required
def add_activity():
    form = ActivityForm()

    if form.validate_on_submit():
        a = Activity(name=capitalize_str(form.name.data),
                     category=capitalize_str(form.category.data))
        db.session.add(a)
        db.session.commit()
        flash('New activity added!', 'success')
        return redirect(url_for('activities', title='Activities'))

    return render_template('add_activity.html', legend='New Activity', form=form)


@app.route('/class/<int:activity_id>', methods=['GET', 'POST'])
@login_required
def activity(activity_id):
    act = Activity.query.get(activity_id)
    form = ActivityForm()

    if act and form.validate_on_submit():
        act.name = capitalize_str(form.name.data)
        db.session.add(act)
        db.session.commit()
        flash('Activity updated!', 'success')

    elif request.method == 'GET':
        form.name.data = act.name
        form.category.data = act.category
        return render_template('add_activity.html', legend='Update activity', form=form)

    return redirect(url_for('activities'))


@app.route('/activity/<int:activity_id>/delete', methods=['POST'])
@login_required
def delete_activity(activity_id):
    act = Activity.query.get(activity_id)
    act_name = act.name

    db.session.delete(act)
    db.session.commit()
    flash(f'{act_name} has been deleted!', 'success')

    return redirect(url_for('activities'))


'''
Attendance related endpoints



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
                             for c in Activity.query.all()]

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
'''

'''
CSV loader

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

                # Add Activity if class doesn't exists
                c = Activity.query.filter_by(name=class_name).first()
                if not c:
                    c = Activity(name=class_name)
                    db.session.add(c)
                    db.session.commit()
                    flash(f'Class {class_name} created from csv', 'success')

                a = Attendance(class_id=c.id, date_attended=date)
                db.session.add(a)
                db.session.commit()
                flash(f'New attendance create for {class_name}', 'success')

        return redirect(url_for('classes'))

    return render_template('upload.html', title='Upload CSV')

    '''
