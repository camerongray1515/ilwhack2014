from django.db import models

class Tweet (models.Model):
    sender = models.CharField(max_length=50)
    body = models.TextField()
    timestamp = models.DateTimeField()
    latitude = models.DecimalField(max_digits=3, decimal_places=7)
    longitude = models.DecimalField(max_digits=3, decimal_places=7)