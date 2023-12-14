from flask import Blueprint, render_template, flash, redirect, url_for, request
from app.classes.forms import ClassForm
from app import db
from app.models import GymClass
from app.classes.utils import capitalize_str


classes = Blueprint("classes", __name__)

# TODO: recover class.html and add_class.html


@classes.route("/classes")
def show_classes():
    page = request.args.get("page", 1, type=int)
    gym_classes = GymClass.query.order_by(GymClass.name).paginate(page=page, per_page=9)
    return render_template("classes.html", title="Classes", gym_classes=gym_classes)


@classes.route("/new_class", methods=["GET", "POST"])
def new_class():
    form = ClassForm()

    if form.validate_on_submit():
        gymclass = GymClass(
            name=capitalize_str(form.name.data),
            class_type=capitalize_str(form.class_type.data),
        )
        db.session.add(gymclass)
        db.session.commit()
        flash("New class added!", "success")
        return redirect(url_for("classes.show_classes", title="Classes"))

    return render_template("add_class.html", legend="New Class", form=form)


@classes.route("/class/<int:class_id>")
def show_class(class_id):
    gymclass = GymClass.query.get(class_id)
    return render_template("class.html", legend=gymclass.name, gymclass=gymclass)


@classes.route("/class/<int:class_id>/update", methods=["GET", "POST"])
def update_class(class_id):
    gymclass = GymClass.query.get(class_id)
    form = ClassForm()

    if gymclass and form.validate_on_submit():
        gymclass.name = capitalize_str(form.name.data)
        db.session.add(gymclass)
        db.session.commit()
        flash("Class updated!", "success")

    elif request.method == "GET":
        form.name.data = gymclass.name
        form.class_type.data = gymclass.class_type
        return render_template("add_class.html", legend="Update class", form=form)

    return redirect(url_for("classes.show_classes"))


@classes.route("/class/<int:class_id>/delete", methods=["POST"])
def delete_class(class_id):
    gymclass = GymClass.query.get(class_id)
    class_name = gymclass.name

    db.session.delete(gymclass)
    db.session.commit()
    flash(f"{class_name} has been deleted!", "success")

    return redirect(url_for("classes.show_classes"))
