from django.db import models

# Create your models here.

from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone
import datetime


class CustomUrl(models.Model):
    """ Model representing mapping bitwing short url and destination url """
    owner = models.ForeignKey(
        User, null=True, blank=True, max_length=20, on_delete=models.CASCADE)
    session = models.ForeignKey(
        Session, null=True, blank=True, on_delete=models.SET_NULL)
    long_url = models.URLField(max_length=2000)
    short_url = models.CharField(primary_key=True, unique=True, max_length=20)
    creation_date = models.DateTimeField(auto_now=True)
    expiration_date = models.DateTimeField(
        null=True, default=timezone.now() + datetime.timedelta(days=30))

    def __str__(self):
        return "{}: {} -> {}".format(self.owner, self.short_url, self.long_url)

    def is_expired(self):
        return timezone.now() >= expiration_date

    @property
    def full_inshort_url(self):
        return "http://127.0.0.1:8000/" + self.short_url

    class Meta:
        ordering = ["owner", "expiration_date"]


class Visit(models.Model):
    """ Model representing history of url visits """
    custom_url = models.ForeignKey(CustomUrl, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now=True)
    visitor_ip = models.GenericIPAddressField(null=True)
    visitor_location = models.CharField(null=True, max_length=200)

    def __str__(self):
        return "{} - {}".format(self.datetime, self.custom_url)

    class Meta:
        ordering = ["custom_url__owner", "datetime"]
