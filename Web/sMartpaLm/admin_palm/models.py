from django.db import models

# Create your models here.

class userPalms(models.Model):
    palm_date = models.DateTimeField()
    title = models.CharField(max_length=30)
    def __str__(self):
        return userPalms.title