from . import auth_blueprint
from flask import render_template, request, redirect, url_for
from ..tasks import send_celery_email

@auth_blueprint.route('/register/<string:email>')
def register(email):
    message_data={
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
  msg = Message('Hello from the other side!', sender =   'me@rezayogaswara.com', recipients = ['reza.yoga@gmail.com'])
  msg.body = "Hey Reza, sending you this email from my Flask app, lmk if it works"
  mail.send(msg)
  return "Message sent!"