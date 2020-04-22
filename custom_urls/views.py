from django.shortcuts import get_object_or_404, get_list_or_404
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User

# Create your views here.

from .models import CustomUrl, Visit

def add_url(request):
    try:
        dest_url = request.POST['dest_url']
        short_url = request.POST['short_url']
        time = request.POST['time']
    except (KeyError, CustomUrl.DoesNotExist):
        # TODO
        return HttpResponse("error")
    else:
        c = CustomUrl(owner=User.objects.get(username=request.user.username), destination_url=dest_url, short_url=short_url)
        c.save()
        return HttpResponseRedirect(reverse('user_urls', args=(request.user.username,)))

def add_url_form(request):
    return render(request, 'urls/add_url_form.html')


def detail(request, short_url):
    custom_url = get_object_or_404(CustomUrl, short_url)
    return HttpResponse("You're looking at custom_url {}.".format(custom_url))


def history(request, short_url):
    custom_url = get_object_or_404(CustomUrl, short_url=short_url)
    response = "You're looking at the results of custom_url {}."
    return HttpResponse(response.format(custom_url))


def user_urls(request, user):
    custom_urls = get_list_or_404(CustomUrl, owner__username=user)
    context = {'user_urls': custom_urls}
    return render(request, 'urls/user_urls.html', context)


def redirect(request, requested_url):
    # Check if requested_url exists
    custom_url = get_object_or_404(CustomUrl, short_url=requested_url)

    # Get visitor ip wheter he's using proxy or not
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    visit = Visit(custom_url=custom_url, visitor_ip=ip)
    visit.save()
    return HttpResponseRedirect(custom_url.destination_url)
