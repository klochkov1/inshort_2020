from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.

from .models import CustomUrl, Visit
from django.http import HttpResponse, HttpResponseRedirect

def detail(request, custom_url_id):
    custom_url = get_object_or_404(CustomUrl, pk=custom_url_id)
    return HttpResponse("You're looking at custom_url {}.".format(custom_url))

def history(request, custom_url_id):
    custom_url = get_object_or_404(CustomUrl, pl=custom_url_id)
    response = "You're looking at the results of custom_url {}."
    return HttpResponse(response.format(custom_url))

def redirect(request, requested_url):
    # Check if requested_url exists
    custom_url = get_object_or_404(CustomUrl, short_url=requested_url)

    #Get visitor ip wheter he's using proxy or not
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    visit = Visit(custom_url=custom_url, visitor_ip=ip)
    visit.save()
    return HttpResponseRedirect(custom_url.destination_url)