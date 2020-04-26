from django.shortcuts import get_object_or_404, get_list_or_404
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, Http404
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.utils import timezone
from .models import CustomUrl, Visit
from .url_generator.rand_string import StringGenerator 


def add_url(request):
    try:
        dest_url = request.POST['source_url']
        short_url = request.POST['short_url']
        time = request.POST['time']
    except (KeyError, CustomUrl.DoesNotExist):
        return HttpResponseBadRequest("Bad request")
    else:
        if not request.session.session_key:
            request.session.create()
        session = Session.objects.get(pk=request.session.session_key)
        print("DEBUG:" + str(session))
        owner = None
        if request.user.is_authenticated:
            owner = User.objects.get(username=request.user.username)
        c = CustomUrl(owner=owner, session=session,
                      source_url=dest_url, short_url=short_url)
        c.save()
        return HttpResponseRedirect(reverse('user_urls'))


def delete_url(request, short_url):
    try:
        short_url = request.POST['short_url']
    except (KeyError, CustomUrl.DoesNotExist):
        return HttpResponseBadRequest("Bad request")
    else:
        c = get_list_or_404(CustomUrl, short_url=short_url)
        c.delete()
        return HttpResponseRedirect(reverse('user_urls'))


def add_url_form(request):
    if not request.session.session_key:
        request.session.create()
    return render(request, 'urls/add_url_form.html')


def history(request, short_url):
    custom_urls = get_list_or_404(Visit, custom_url__short_url=short_url)
    context = {'visits': custom_urls}
    return render(request, 'urls/url_history.html', context)


def user_urls(request):
    if request.user.is_authenticated:
        custom_urls = get_list_or_404(
            CustomUrl, owner__username=request.user.username)
        visits = []
    else:
        # REMAKE
        if not request.session.session_key: raise Http404()
        custom_urls = get_list_or_404(
            CustomUrl, session__pk=request.session.session_key)
        visits = []
    context = {'user_urls': custom_urls, 
               'visits': visits }
    return render(request, 'urls/user_urls.html', context)


def redirect(request, requested_url):
    # Check if requested_url exists
    custom_url = get_object_or_404(CustomUrl, short_url=requested_url)
    # Check expiration
    if custom_url.expiration_date <= timezone.now():
        # custom_url.delete()
        raise Http404("Заданого посилання не існує")
    # Get visitor ip wheter he's using proxy or not
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    visit = Visit(custom_url=custom_url, visitor_ip=ip)
    visit.save()
    return HttpResponseRedirect(custom_url.source_url)
