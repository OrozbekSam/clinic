from django.db import models
from django.utils.text import slugify
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.contrib.auth import get_user_model

User = get_user_model()


class Medicine(models.Model):
    type = models.CharField(max_length=30, unique=True)
    description = models.TextField()

    class Meta:
        ordering = ['type']

    def __str__(self):
        return self.type


class Doctor(models.Model):
    
    Gender = (
        ('M', 'Man'),
        ('W', 'Woman'),
    )

    image = models.ImageField(upload_to='images')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=5, choices=Gender)
    category = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='doctor')
    experience_year = models.PositiveIntegerField()
    about = models.TextField()
    holiday = models.BooleanField()   # Врач находится в отпуске, поэтому время приема недоступно.

    def __str__(self):
        return f'Dc.{self.first_name} {self.last_name}'


class Comment(models.Model):
    owner = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.owner}-> {self.doctor} -> {self.created_at}'


class Likes(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked')

    class Meta:
        unique_together = ['doctor', 'user']


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='favorites')

    def __str__(self): return f"{self.user}'s favorite: {self.doctor}"
