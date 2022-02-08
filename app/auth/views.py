from . import auth_blueprint
from flask import render_template, request, redirect, url_for, current_app
from ..tasks import send_celery_email, mail
from flask_mail import Message
import bugsnag


@auth_blueprint.route('/register/<string:email>')
def register(email):
    message_data = {
        'subject': 'Hello from the flask app!',
        'body': 'This email was sent asynchronously using Celery.',
        'recipients': email,

    }
    send_celery_email.apply_async(args=[message_data])
    return render_template('auth/register.html', email=email)


@auth_blueprint.route('/login/')
def login():
    return render_template('auth/login.html')


@auth_blueprint.route("/")
def index():
    app = current_app._get_current_object()
    msg = Message('Hello from the other side!',
                  sender=("Reza Yogaswara",
                          app.config['MAIL_DEFAULT_SENDER']),
                  recipients=['admin@komunitassahabatsehat.com'])
    msg.body = "Hey Reza, sending you this email from my Flask app, lmk if it works"
    mail.send(msg)
    bugsnag.notify(Exception('Test mail sent'))
    return "Message sent!"
