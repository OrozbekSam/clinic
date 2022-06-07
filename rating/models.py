from django.db import models
from doctor.models import Doctor
from django.contrib.auth import get_user_model

User = get_user_model()


class Mark():
    one = 1
    two = 2
    three = 3
    four = 4
    five = 5

    marks = (
        (one, 'Очень плохо!'),
        (two, 'Плохо'),
        (three, 'Удовлетворительно!'),
        (four, 'Хорошо!'),
        (five, 'Отлично!'),
    )


class Rating(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='ratings')
    mark = models.PositiveSmallIntegerField(choices=Mark.marks)

    def __str__(self):
        return f'{self.mark} -> {self.doctor}'

    class Meta:
        unique_together = ('owner', 'doctor')
