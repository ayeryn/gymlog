from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

# Python module secrets
app.config["SECRET_KEY"] = "85d7836bac21fafd3ed57a1d18c06518"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

db = SQLAlchemy(app)

activities = [
    {
        'name': 'swimming',
        'category': 'cardio'
    },
    {
        'name': 'upper body training',
        'category': 'strength'
    },
    {
        'name': 'vinyasa',
        'category': 'yoga'
    },
    {
        'name': 'incline hike',
        'category': 'cardio'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", activities=activities)


@app.route("/about")
def about():
    return render_template("about.html", title='About')


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for("home"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'test@a.com' and form.password.data == "12345":
            flash(f"You have been logged in!", "success")
            return redirect(url_for("home"))
        else:
            flash(f"Login unsuccessful! Please check username and password", "danger")
    return render_template("login.html", title="Login", form=form)


if __name__ == "__main__":
    app.run(debug=True)
