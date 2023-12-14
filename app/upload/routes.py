from flask import Blueprint, render_template, flash, redirect, url_for, request
from io import TextIOWrapper
import os
import csv
from app import db
from app.models import GymClass, Attendance
from app.upload.utils import process_csv_row


upload = Blueprint("upload", __name__)

ALLOWED_EXTENSIONS = set([".csv"])


@upload.route("/upload", methods=["GET", "POST"])
def upload_csv():
    if request.method == "POST":
        file = request.files["file"]
        f_name, f_ext = os.path.splitext(file.filename)

        if file and f_ext in ALLOWED_EXTENSIONS:
            file = TextIOWrapper(file, encoding="utf-8")
            csv_reader = csv.reader(file, delimiter=",")
            for row in csv_reader:
                class_name, date = process_csv_row(row, f_name)

                # Add GymClass if class doesn't exists
                c = GymClass.query.filter_by(name=class_name).first()
                if not c:
                    c = GymClass(name=class_name)
                    db.session.add(c)
                    db.session.commit()
                    flash(f"Class {class_name} created from csv", "success")

                a = Attendance(class_id=c.id, date_attended=date)
                db.session.add(a)
                db.session.commit()
                flash(f"New attendance create for {class_name}", "success")

        return redirect(url_for("classes.show_classes"))

    return render_template("upload.html", title="Upload CSV")
