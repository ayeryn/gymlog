from datetime import date
from app.classes.utils import capitalize_str


def process_csv_row(data, filename):
    year = filename[:4]
    month = filename[4:]

    # Parse row
    day = data[0]
    class_name = capitalize_str(data[1])

    date_attended = date(int(year), int(month), int(day))
    return class_name, date_attended
