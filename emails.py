from flask import current_app, render_template
import sendgrid
import threading
import os

sg = sendgrid.SendGridClient(os.environ['SENDGRID_USERNAME'], os.environ['SENDGRID_PASSWORD'])

## Code from https://github.com/lingthio/Flask-User/blob/master/flask_user/emails.py
def render_email(filename, **kwargs):
    # Render HTML message
    html_message = render_template(filename+'.html', **kwargs)
    # Render text message
    text_message = render_template(filename+'.txt', **kwargs)

    return (html_message, text_message)

def send_email(recipient, subject, html_message, text_message):
    message = sendgrid.Mail()
    message.add_to(recipient)
    message.set_subject(subject)
    message.set_html(html_message)
    message.set_text(text_message)
    message.set_from('flaskAPI@github.com')
    sg.send(message)

def send_activate_account_email(user_email, token):
    activate_account_link = 'http://localhost:5000/activate_account/' + token
    # Render subject, html message and text message
    subject = 'Action required: Activate Your Account!'
    html_message, text_message = render_email('activate_account', activate_account_link=activate_account_link)

    threading.Thread(target=send_email, args=(user_email, subject, html_message, text_message)).start()
