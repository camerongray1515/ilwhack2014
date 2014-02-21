from django.db import models


class Tweet(models.Model):
    sender = models.CharField(max_length=50)
    body = models.TextField()
    timestamp = models.DateTimeField()
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)


class HappinessScore(models.Model):
    tweet = models.OneToOneField(Tweet)
    polarity = models.DecimalField(max_digits=2, decimal_places=1)
    subjectivity = models.DecimalField(max_digits=2, decimal_places=1)


class DataZone(models.Model):
    code = models.CharField(max_length=9)
    name = models.CharField(max_length=255)
    polygon = models.TextField()

class TweetLocation(models.Model):
    zone = models.ForeignKey(DataZone)
    tweet = models.OneToOneField(Tweet)