from django.core.mail import send_mail

from clinic.celery import app
from .send_email import send_confirmation_email


@app.task
def send_activation_code(to_email, code):
        full_link = f'http://localhost:8000/api/v1/account/activate/{code}'
        send_mail('Здравствуйте активируйте ваш аккаунт!',
                  f"Что-бы активировать ваш аккаунт нужно перейти по ссылке {full_link}",
                  'from@example.com',
                  [to_email],
                  fail_silently=False, )