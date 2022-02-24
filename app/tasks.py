from flask_mail import Message
from . import mail, celery
from flask import current_app


@celery.task(name='app.tasks.send_celery_email')
def send_celery_email(message_data):
    app = current_app._get_current_object()
    message = Message(subject=message_data['subject'],
                      recipients=[message_data['recipients']],
                      body=message_data['body'],
                      sender=("Reza Yogaswara",
                              app.config['MAIL_DEFAULT_SENDER']))

    mail.send(message)


@celery.task(name='app.task.find_fibonacci_assync')
def find_fibonacci_async(number):
    def fib(n):
        if n == 1:
            return 0
        if n == 2:
            return 1

        return fib(n-1)+fib(n-2)
    result = fib(number)
    return result
