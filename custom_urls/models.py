from django.db import models

# Create your models here.

from django.utils import timezone
from django.contrib.auth.models import User


class CustomUrl(models.Model):
    """ Model representing mapping bitwing short url and destination url """
    owner = models.ForeignKey(
        User, null=True, blank=True, max_length=20, on_delete=models.CASCADE)
    destination_url = models.URLField(max_length=2000)
    short_url = models.CharField(unique=True, max_length=20)
    description = models.CharField(null=True, blank=True, max_length=255)
    creation_date = models.DateTimeField(auto_now=True)
    expiration_date = models.DateTimeField(null=True, auto_now=False)

    def __str__(self):
        return "{}: {} -> {}".format(self.owner, self.short_url, self.destination_url)

    def is_expired(self):
        return timezone.now() >= expiration_date

    class Meta:
        ordering = ["owner", "expiration_date"]


class Visit(models.Model):
    """ Model representing history of url visits """
    custom_url = models.ForeignKey(CustomUrl, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now=True)
    visitor_ip = models.GenericIPAddressField(null=True)
    visitor_location = models.CharField(null=True, max_length=200)

    def __str__(self):
        return "{} - {}".format(self.visit_datetime, self.custom_url)

    class Meta:
        ordering = ["custom_url__owner", "datetime"]
