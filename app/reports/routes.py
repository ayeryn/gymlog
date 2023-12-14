from flask import Blueprint, render_template
from datetime import date
from sqlalchemy import extract
from collections import defaultdict
from app.models import Attendance


reports = Blueprint("reports", __name__)


@reports.route("/monthly_report")
def monthly_report():
    today = date.today()
    attendances = Attendance.query.filter(
        extract("year", Attendance.date_attended) == today.year
    ).filter(extract("month", Attendance.date_attended) == today.month)

    data = defaultdict(int)
    for attendance in attendances:
        data[attendance.class_taken.name] += 1

    labels = [k for k in data.keys()]
    values = [v for v in data.values()]

    return render_template("monthly_report.html", labels=labels, values=values)


@reports.route("/yearly_report")
def yearly_report():
    attendances = Attendance.query.filter(
        extract("year", Attendance.date_attended) == date.today().year
    )

    data = defaultdict(int)
    for attendance in attendances:
        data[attendance.class_taken.name] += 1

    labels = [k for k in data.keys()]
    values = [v for v in data.values()]

    return render_template("yearly_report.html", labels=labels, values=values)
