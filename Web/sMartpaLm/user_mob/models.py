from django.db import models

# Create your models here.
class userPalms(models.Model):
    title = models.CharField(max_length=30)
    palm_date = models.DateTimeField()
    def __str__(self):
        return userPalms.title