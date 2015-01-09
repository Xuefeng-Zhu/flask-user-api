from flask import current_app, render_template
from flask_mail import Message

## Code from https://github.com/lingthio/Flask-User/blob/master/flask_user/emails.py
def render_email(filename, **kwargs):
    # Render HTML message
    html_message = render_template(filename+'.html', **kwargs)
    # Render text message
    text_message = render_template(filename+'.txt', **kwargs)

    return (html_message, text_message)

def send_email(recipient, subject, html_message, text_message):
    mail_engine = current_app.extensions.get('mail')
    message = Message(subject, recipients=[recipient], html = html_message, body = text_message)
    mail_engine.send(message)

def send_activate_account_email(user_email, token):
    activate_account_link = 'http://localhost:5000/activate_account/' + token
    
    # Render subject, html message and text message
    subject = 'Action required: Activate Your Account!'
    html_message, text_message = render_email('activate_account', activate_account_link=activate_account_link)

    send_email(user_email, subject, html_message, text_message)
