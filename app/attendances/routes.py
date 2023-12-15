from flask import Blueprint, render_template, flash, redirect, url_for, request
from app import db
from app.models import GymClass, Attendance
from app.attendances.forms import AttendanceForm


attendances = Blueprint("attendances", __name__)


@attendances.route("/attendances")
def show_attendances():
    page = request.args.get("page", 1, type=int)
    attendance_list = Attendance.query.order_by(
        Attendance.date_attended.desc()
    ).paginate(page=page, per_page=15)
    return render_template(
        "attendances.html", title="Attendances", attendance_list=attendance_list
    )


@attendances.route("/new_attendance", methods=["GET", "POST"])
def new_attendance():
    form = AttendanceForm()
    form.class_id.choices = [(c.id, c.name) for c in GymClass.query.all()]

    class_id = request.args.get("class_id")
    if class_id:
        form.class_id.data = int(class_id)

    if form.validate_on_submit():
        a = Attendance(
            class_id=form.class_id.data, date_attended=form.date_attended.data
        )
        db.session.add(a)
        db.session.commit()
        flash(f"New attendance added for {a.class_taken.name}!", "success")
        return redirect(url_for("classes.show_class", class_id=a.class_id))

    return render_template("add_attendance.html", legend="New Attendance", form=form)


@attendances.route("/attendance/<int:attendance_id>/update", methods=["GET", "POST"])
def edit_attendance(attendance_id):
    a = Attendance.query.get(attendance_id)
    form = AttendanceForm()

    if a and form.validate_on_submit():
        a.class_id = form.class_id.data
        a.date_attended = form.date_attended.data
        db.session.add(a)
        db.session.commit()
        flash("Attendance updated!", "success")
    elif request.method == "GET":
        form.class_id.data = a.class_taken.name
        form.date_attended.data = a.date_attended
        return render_template(
            "add_attendance.html", legend="Update Attendance", form=form
        )

    return redirect(url_for("attendances.show_attendances"))


@attendances.route("/attendance/<int:attendance_id>/delete", methods=["POST"])
def delete_attendance(attendance_id):
    a = Attendance.query.get(attendance_id)
    db.session.delete(a)
    db.session.commit()
    flash(f"Attendance has been deleted!", "success")

    return redirect(url_for("attendances.show_attendances"))
