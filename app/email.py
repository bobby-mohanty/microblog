"""Wrapper function for sending emails."""

from app import app, mail

from threading import Thread
from flask import render_template
from flask_mail import Message


def send_async_email(app, msg):
    """Send async email."""
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body=None, html_body=None):
    """Wrapper to send email."""
    msg = Message(subject, sender=sender, recipients=recipients)
    if not text_body:
        text_body = "TEST MAIL"
    msg.body = text_body
    if html_body:
        msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()


def send_password_reset_email(user):
    """Send password rest mail with token."""
    token = user.get_reset_password_token()
    send_email('[Microblog] Reset Your Password',
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))
