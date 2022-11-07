from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.

# class Post(models.Model):
#     stegtype = models.CharField(max_length=20)
#     hiddentext = models.TextField(max_length=60)
#     date = models.DateTimeField(default=timezone.now)
#     stegtext = models.CharField(max_length=300)
#     stegimage = models.ImageField(default='default.jpeg', upload_to='steg_image')
#     author = models.ForeignKey(User, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.stegtype


class PostFile(models.Model):
    name = models.FileField(upload_to='client')
    date = models.DateTimeField(default=timezone.now)
    file_hidden = models.TextField(max_length=255)
    state = models.CharField(max_length=15)
    type_file_list = (
        ('', 'Selectionner une option'),
        ('1', 'images(.jpeg, .jpg, .png)'),
        ('2', 'audio(.wav, .mp3)'),
        ('3', 'videos(.mp4, .avi)')
    )
    type_file_id = models.CharField(max_length=70, choices=type_file_list, default="Selectionner une option")

    def __str__(self):
        return self.name
