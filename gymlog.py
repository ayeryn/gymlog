from flask import Flask, render_template, url_for

app = Flask(__name__)

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


if __name__ == '__main__':
    app.run(debug=True)
