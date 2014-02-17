from django.db import models

from twitter.models import Tweet

class HappinessScore (models.Model):
    tweet = models.OneToOneField(Tweet)
    polarity = models.DecimalField(max_digits=2, decimal_places=1)
    subjectivity = models.DecimalField(max_digits=2, decimal_places=1)