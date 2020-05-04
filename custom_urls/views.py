from django.shortcuts import get_object_or_404, get_list_or_404
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, Http404
from django.http import JsonResponse
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.utils import timezone
from .models import CustomUrl, Visit, is_valid_status
import json
from django.views.decorators.csrf import csrf_exempt


def add_url(request):
    try:
        dest_url = request.POST['long_url'].strip()
        short_url = request.POST['short_url'].strip()
        min_active = int(request.POST['time'])
    except (KeyError, CustomUrl.DoesNotExist):
        return HttpResponseBadRequest("Bad request")
    else:
        owner = None
        session = None
        if request.user.is_authenticated:
            owner = User.objects.get(username=request.user.username)
        else:
            if not request.session.session_key:
                request.session.create()
            session = Session.objects.get(pk=request.session.session_key)
        CustomUrl.create(owner=owner, session=session,
                         long_url=dest_url, short_url=short_url, min_active=min_active, active=True)
        return HttpResponseRedirect(reverse('home'))


def get_new_shortin(request):
    url = CustomUrl.get_random_url()
    return JsonResponse({'url': url})


@csrf_exempt
def check_url(request):
    if request.method == 'POST':
        url = json.loads(request.body).get('url', '')
        is_valid, status = CustomUrl.is_valid_url(url)
        return JsonResponse({'is_valid':is_valid, 'status':is_valid_status[status]})
    return HttpResponseRedirect(reverse('home'))


def delete_url(request, short_url):
    try:
        short_url = request.POST['short_url']
    except (KeyError, CustomUrl.DoesNotExist):
        return HttpResponseBadRequest("Bad request")
    else:
        c = get_list_or_404(CustomUrl, short_url=short_url)
        c.delete()
        return HttpResponseRedirect(reverse('user_urls'))


def user_urls(request):
    if request.user.is_authenticated:
        custom_urls = get_list_or_404(
            CustomUrl, owner__username=request.user.username)
    else:
        if not request.session.session_key:
            raise Http404()
        custom_urls = get_list_or_404(
            CustomUrl, session__pk=request.session.session_key)
    context = {'user_urls': custom_urls}
    return render(request, 'urls/user_urls.html', context)


def redirect(request, requested_url):
    # Check if requested_url exists
    #custom_url = get_object_or_404(CustomUrl, short_url=requested_url, active=True)
    # Check expiration
    custom_url = CustomUrl.objects.filter(short_url=requested_url, active=True)
    if len(custom_url) == 0:
        return render(request, "urls/404.html", {"url":requested_url})
    if custom_url.expiration_date <= timezone.now():
        custom_url.delete()
        return render(request, "urls/404.html", {"url":requested_url})
    #   raise Http404("Заданого посилання не існує")
    # Get visitor ip wheter he's using proxy or not
    Visit.log_visit(custom_url=custom_url, request=request)
    return HttpResponseRedirect(custom_url.long_url)
