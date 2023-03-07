from flask import Flask

app = Flask(__name__)


# If multiple routes point to the same page,
# add another decorator to the same function
@app.route('/')
@app.route('/home')
def home():
    return "<h1>Home!</h1>"


@app.route("/about")
def about():
    return "<h1> About Page</h1>"


# When python runs a program directly, the module name
# is __main__
if __name__ == '__main__':
    app.run(debug=True)
