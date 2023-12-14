from flask_mail import Message
from flask import render_template
from app import mail, app


def send_email(subject, recipients, text_body, html_body):
    msg = Message(subject,
                  sender='noreply@gymlog.me',
                  recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[GYMLOG]Reset Your Password',
               [user.email],
               render_template('email/reset_password.txt',
                               user=user, token=token),
               render_template('email/reset_password.html',
                               user=user, token=token))
