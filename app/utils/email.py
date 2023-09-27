from threading import Thread

from flask import current_app
from flask_mail import Message

from extensions.email import mail


def send_email_async(to, subject, template):
    msg = Message(subject, 
                  recipients=[to], 
                  html=template, 
                  sender=('Discussify', 'api.discussify@gmail.com'))
    
    mail.send(msg)


def send_email(to, subject, template):
    email_thread = Thread(target=send_email_async, args=(to, subject, template))
    email_thread.start()