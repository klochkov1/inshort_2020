from django.db import models

# Create your models here.

from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone
from .url_generator.fixed_string import is_walid_url, RandFixedLenStrStorage as RandStr
from django.db.models.functions import Length
import datetime

def get_default_expire_date():
    return timezone.now() + datetime.timedelta(days=30)

class CustomUrl(models.Model):
    """ Model representing mapping bitwing short url and destination url """
    owner           = models.ForeignKey(
        User, null=True, blank=True, max_length=20, on_delete=models.CASCADE)
    session         = models.ForeignKey(
        Session, null=True, blank=True, on_delete=models.SET_NULL)
    long_url        = models.URLField(max_length=2000)
    short_url       = models.CharField(primary_key=True, unique=True, max_length=20)
    creation_date   = models.DateTimeField(auto_now=True)
    expiration_date = models.DateTimeField(
        null=True, default=get_default_expire_date)
    is_active       = models.BooleanField()

    @classmethod
    def clear_expired(cls):
        cls.objects.filter(expiration_date__lte=timezone.now(), is_active=True).update(is_active=False)

    @classmethod
    def get_random_url(cls, def_len = 4):
        cur_len = def_len
        cur_list = cls.get_all_active_url_with_len(cur_len)
        cur_gen = RandStr(cur_len, cur_list)
        while cur_gen.is_overflowed:
            cur_len += 1
            cur_list = cls.get_all_active_url_with_len(cur_len)
            cur_gen = RandStr(cur_len, cur_list)
        return cur_gen.get_random_word()

    @classmethod
    def get_all_active_url_with_len(cls, url_length):
        return cls.objects.annotate(url_len=Length('short_url')).filter(url_len=4, is_active=True).\
            values_list("short_url", flat=True).order_by("short_url")

    @classmethod
    def try_add_url(cls, url, redirect_url, user=None, min_active=60):
        is_free = cls.is_word_unused(url)
        if is_free:
            t_expired = timezone.now() + timezone.timedelta(minutes=min_active)
            u_active = cls()
            if user is not None and not user.is_anonymous:
                u_active.owner = user
            else:
                u_active.owner = None
            u_active.long_url  = redirect_url
            u_active.short_url        = url
            u_active.expiration_date  = t_expired
            u_active.is_active        = True
            u_active.save()
        return is_free

    @classmethod
    def is_word_unused(cls, word):
        if not is_walid_url(word):
            raise Exception(f"Word {word} is not walid")
        return cls.objects.filter(short_url=word, is_active=True).count() == 0

    @classmethod
    def get_all_in_dict_list_with_visits(cls, user):
        if user is None or user.is_anonymous:
            return None
        query = CustomUrl.objects.filter(owner=user)
        res = []
        for i in query:
            if i.is_expired(): 
                i.is_active = False
                i.save()
            cur_dict = {}
            cur_dict["owner_username"]   = i.owner.username
            cur_dict["long_url"]  = i.long_url
            cur_dict["short_url"]        = i.short_url      
            cur_dict["creation_date"]    = i.creation_date  
            cur_dict["expiration_date"]  = i.expiration_date
            cur_dict["is_active"]        = i.is_active 
            hist = list(Visit.objects.filter(custom_url=i).values("visitor_ip", "datetime", "visitor_location"))     
            cur_dict["attempt_hist"]     = hist
            res.append(cur_dict)
        return res

    def __str__(self):
        return "{}: {} -> {}".format(self.owner, self.short_url, self.long_url)

    def is_expired(self):
        return timezone.now() >= self.expiration_date

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

    @classmethod
    def get_redir__by_hist(cls, history):
        return [(i.visitor_ip, i.datetime) for i in cls.get_redir_by_hist(history)]

    @classmethod
    def get_redir_by_hist(cls, history):
        return cls.objects.filter(hist=history)\

    @staticmethod
    def get_ip_from_request(request):
        forwaded = request.META.get('HTTP_X_FORWARDED_FOR')
        if forwaded:
            ip = forwaded(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    @classmethod
    def get_redirect_url(cls, short_url, request):
        query = CustomUrl.objects.filter(short_url=short_url, is_active=True)
        q_len = len(query)
        if q_len == 0:
            return None
        elif q_len == 1:
            custom_url = query[0]
            url_redir = cls()
            url_redir.custom_url = custom_url
            url_redir.visitor_ip = cls.get_ip_from_request(request)
            url_redir.save()
            return custom_url.short_url
        else:
            raise Exception(f"there is {q_len} active short url, must be one")

    def __str__(self):
        return "{} - {}".format(self.datetime, self.custom_url)

    class Meta:
        ordering = ["custom_url__owner", "datetime"]
