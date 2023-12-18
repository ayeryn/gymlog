import secrets
import os
from PIL import Image
from flask_mail import Message
from flask import render_template
from app import app, mail


def save_picture_data(form_picture):
    # generate hashed name to avoid collision
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    filename = random_hex + f_ext

    # generate absolute path for profile pic
    filepath = os.path.join(app.root_path, "static/profile_pics", filename)

    # resize pic to icon size before saving
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(filepath)

    return filename


def remove_old_pic(filename):
    filename = os.path.join(app.root_path, "static/profile_pics", filename)
    try:
        os.remove(filename)
    except Exception as e:
        print(f"An error occurred: {e}!")


def send_email(subject, recipients, text_body, html_body, sender="noreply@gymlog.me"):
    msg = Message(subject, sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email(
        "[GYMLOG]Reset Your Password",
        [user.email],
        render_template("email/reset_password.txt", user=user, token=token),
        render_template("email/reset_password.html", user=user, token=token),
    )
