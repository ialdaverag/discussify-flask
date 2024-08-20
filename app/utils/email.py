# threading
from threading import Thread

# Flask
from flask import current_app

# Flask-Mail
from flask_mail import Message

# Extensions
from app.extensions.email import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template):
    app = current_app._get_current_object()
    
    msg = Message(
        subject, 
        recipients=[to], 
        html=template, 
        sender=('Discussify', 'api.discussify@gmail.com')
    )

    Thread(target=send_async_email, args=(app, msg)).start()