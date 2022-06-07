from django.contrib.auth import get_user_model
from django.db import models

from account.send_email import send_notification
from doctor.models import Doctor
from django.dispatch import receiver
from django.db.models.signals import post_save

User = get_user_model()
STATUS_CHOICES = (
    ('open', 'Открыт'),
    ('in_check', 'Проверяться'),
    ('closed', 'Закрыт'),
)


class AppointmentItem(models.Model):
    Gender = (
        ('M', 'Man'),
        ('W', 'Woman'),
    )

    DAYS = (
      ('Mon', 'Понедельник'),
      ('Tue', 'Вторник'),
      ('Wed', 'Среда'),
      ('Thu', 'Четверг'),
      ('Fri', 'Пятница'),
    )

    TIMESLOT_LIST = (
        (1, '09:00 – 10:00'),
        (2, '10:00 – 11:00'),
        (3, '11:00 – 12:00'),
        (4, '12:00 – 13:00'),
        (5, '13:00 – 14:00'),
        (6, '14:00 – 15:00'),
        (7, '15:00 – 16:00'),
        (8, '16:00 – 17:00'),
        (9, '17:00 – 18:00'),
    )
    appointment = models.ForeignKey('Appointment', related_name='items', on_delete=models.RESTRICT)
    doctor = models.ForeignKey(Doctor, on_delete=models.RESTRICT)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    gender = models.CharField(max_length=5, choices=Gender)
    date_birth = models.DateField()
    body = models.TextField()
    phone_number = models.CharField(max_length=13)
    email = models.EmailField()
    address = models.CharField(max_length=50)
    days = models.CharField(max_length=5, choices=DAYS)
    timeslot = models.IntegerField(choices=TIMESLOT_LIST)

    class Meta:
        unique_together = ('days', 'doctor', 'timeslot')
    
    def __str__(self): return f"{self.email} -> {self.doctor}"


class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='appointments')
    doctor = models.ManyToManyField(Doctor, through=AppointmentItem)
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)

    class Meta:
        ordering = ('created_at',)

    def __str__(self): return f"{self.user} -> {self.status}"


@receiver(post_save, sender=Appointment)
def order_post_save(sender, instance, *args, **kwargs):
    send_notification(instance.user, instance.id)
