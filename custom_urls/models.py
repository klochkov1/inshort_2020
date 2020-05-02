from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.http import Http404
from django.utils import timezone
from .url_generator.fixed_string import is_walid_url, RandFixedLenStrStorage as RandStr
from django.db.models.functions import Length
import datetime

def get_expire_date(minutes=10080):
    return timezone.now() + timezone.timedelta(minutes=minutes)

#for backward compatibility, remove after migrating from sqlite
def get_default_expire_date(minutes=10080):
    return timezone.now() + datetime.timedelta(minutes=10080)

reserved_url = {"home", "accounts", "admin", "urls"}

is_valid_status = {0:"Ok", 1:"short url is empty string", 2:"short url is reserved", 3:"short url is not match alphabet", 4:"short url is already used"}


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
        null=True, default=get_expire_date)
    active = models.BooleanField()

    @classmethod
    def create(cls, min_active, *args, **kwargs):
        if min_active:
            if min_active == -1:
                exp_date = None
            else:   
                exp_date = get_expire_date(min_active)
                print(exp_date)
        if not "short_url" in kwargs:
            raise ValueError("short_url required.")
        else:
            is_valide, status = cls.is_valid_url(kwargs["short_url"])
            if not is_valide:
                raise Exception(is_valid_status[status])
        print(exp_date)
        custom_url = cls(expiration_date=exp_date, *args, **kwargs)
        custom_url.save()
        return custom_url

    @classmethod
    def is_valid_url(cls, url):
        "return (is_valid, status)"
        if url is None or len(url) == 0:
            return (False, 1)
        elif url in reserved_url:
            return (False, 2)
        elif not is_walid_url(url):
            return (False, 3)
        elif CustomUrl.objects.filter(short_url=url, active=True).exists():
            return (False, 4)
        return (True, 0)

    @classmethod
    def clear_expired(cls):
        cls.objects.filter(expiration_date__lte=timezone.now(),
                           active=True).update(active=False)

    @classmethod
    def get_random_url(cls, def_len=4):
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
        return cls.objects.annotate(url_len=Length('short_url')).filter(url_len=4, active=True).\
            values_list("short_url", flat=True).order_by("short_url")

    @classmethod
    def try_add_url(cls, url, redirect_url, user=None, min_active=60):
        is_free = not CustomUrl.objects.filter(pk=url).exists()
        if is_free:
            t_expired = timezone.now() + timezone.timedelta(minutes=min_active)
            u_active = cls()
            if user is not None and not user.is_anonymous:
                u_active.owner = user
            else:
                u_active.owner = None
            u_active.long_url = redirect_url
            u_active.short_url = url
            u_active.expiration_date = t_expired
            u_active.active = True
            u_active.save()
        return is_free

    @classmethod
    def get_all_in_dict_list_with_visits(cls, user):
        if user is None or user.is_anonymous:
            return None
        query = CustomUrl.objects.filter(owner=user)
        res = []
        for i in query:
            if i.is_expired():
                i.active = False
                i.save()
            cur_dict = {}
            cur_dict["owner_username"] = i.owner.username
            cur_dict["long_url"] = i.long_url
            cur_dict["short_url"] = i.short_url
            cur_dict["creation_date"] = i.creation_date
            cur_dict["expiration_date"] = i.expiration_date
            cur_dict["active"] = i.active
            hist = list(Visit.objects.filter(custom_url=i).values(
                "visitor_ip", "datetime", "visitor_location"))
            cur_dict["attempt_hist"] = hist
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
        ordering = ["active", "owner", "expiration_date"]


class Visit(models.Model):
    """ Model representing history of url visits """
    custom_url = models.ForeignKey(CustomUrl, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now=True)
    visitor_ip = models.GenericIPAddressField(null=True)
    visitor_location = models.CharField(null=True, max_length=200)

    @classmethod
    def log_visit(cls, request, custom_url):
        ip = cls.get_ip_from_request(request)
        visit = Visit(custom_url=custom_url, visitor_ip=ip)
        visit.save()

    @staticmethod
    def get_ip_from_request(request):
        forwaded = request.META.get('HTTP_X_FORWARDED_FOR')
        if forwaded:
            ip = forwaded.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    @classmethod
    def get_redirect_url(cls, short_url, request):
        custom_url = CustomUrl.objects.get(pk=short_url)
        if not custom_url.active:
            raise Http404(
                "Заданого посилання не існує або воно більше не є дійсним.")
        url_redir = cls()
        url_redir.custom_url = custom_url
        url_redir.visitor_ip = get_ip_from_request(request)
        url_redir.save()
        return custom_url.short_url

    def __str__(self):
        return "{} - {}".format(self.datetime, self.custom_url)

    class Meta:
        ordering = ["custom_url__owner", "datetime"]
