from django.core.mail import send_mail


def send_confirmation_email(user):
    code = user.activation_code
    full_link = f'http://localhost:8000/api/v1/account/activate/{code}'
    to_email = user.email
    send_mail('Здравствуйте активируйте ваш аккаунт!',
              f"Что-бы активировать ваш аккаунт нужно перейти по ссылке {full_link}",
              'from@example.com',
              [to_email],
              fail_silently=True,)


def send_reset_password(user):
    code = user.activation_code
    to_email = user.email
    send_mail(
        'Восстановление пароля',
        f'Your code: {code}',
        'from@example.com',
        [to_email],
        fail_silently=False,
    )


def send_notification(user, id):
    to_email = user.email
    send_mail(
        'Уведомление о создании записи!',
        'Вы удачно записались. Приходите без опозданий к указанному времени.',
        'market.place@gmail.com',
        [to_email],
        fail_silently=False,
    )