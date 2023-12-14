from flask import Blueprint, render_template
from app.main.utils import get_quote


main = Blueprint("main", __name__)


@main.route("/")
@main.route("/home")
def home():
    quote, author = get_quote()
    return render_template("home.html", quote=quote, author=author)
