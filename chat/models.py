from django.db import models
from datetime import datetime


class Room(models.Model):
    name = models.CharField(max_length=1000)

    def __str__(self): return self.name


class Message(models.Model):
    text = models.TextField()
    date = models.DateTimeField(default=datetime.now, blank=True)
    user = models.CharField(max_length=150)
    room = models.CharField(max_length=150)

    def __str__(self): return f'from:{self.user} ({self.date})'
