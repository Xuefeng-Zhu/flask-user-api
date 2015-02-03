from flask import current_app, render_template
from flask_mail import Message

# Code from
# https://github.com/lingthio/Flask-User/blob/master/flask_user/emails.py


def render_email(filename, **kwargs):
    """
    Render email message in HTML and raw format
    """
    html_message = render_template(filename + '.html', **kwargs)
    text_message = render_template(filename + '.txt', **kwargs)

    return (html_message, text_message)


def send_email(recipient, subject, html_message, text_message):
    """
    Send the email to a specific recipient
    """
    mail_engine = current_app.extensions.get('mail')
    message = Message(
        subject, recipients=[recipient], html=html_message, body=text_message)
    mail_engine.send(message)


def send_activate_account_email(user_email, token):
    """
    Send an email with a link letting the user's account
    """
    activate_account_link = 'http://localhost:5000/activate_account?token=' + \
        token

    subject = 'Action Required: Activate Your Account!'
    html_message, text_message = render_email(
        'activate_account', activate_account_link=activate_account_link)

    send_email(user_email, subject, html_message, text_message)


def send_forget_password_email(user_email, token):
    """
    Send an email with a link letting the user to reset password
    """
    forget_password_link = 'http://localhost:5000/forget_password?token=' + \
        token

    subject = 'Alerts: You Requested to Reset Your Password!'
    html_message, text_message = render_email(
        'forget_password', forget_password_link=forget_password_link)

    send_email(user_email, subject, html_message, text_message)
