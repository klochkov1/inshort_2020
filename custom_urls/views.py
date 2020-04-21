from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.

from .models import CustomUrl, VisitsHistory
from django.http import HttpResponse, HttpResponseRedirect

def detail(request, custom_url_id):
    return HttpResponse("You're looking at custom_url {}.".format(custom_url_id))

def history(request, custom_url_id):
    response = "You're looking at the results of custom_url {}."
    return HttpResponse(response.format(custom_url_id))

def redirect(request, requested_url):
    custom_url = get_object_or_404(CustomUrl, short_url=requested_url)
    return HttpResponseRedirect(custom_url.destination_url)
