from django.shortcuts import render
from django.core.mail import EmailMessage
import json
from django.http import JsonResponse

# Create your views here.

from django.http import HttpResponse


def index(request):
    return render(request, "index.html")

def FAQ(request):
    if request.method == 'POST':
        body_messege = json.loads(request.body).get('message', '')
        email = EmailMessage('Subject', 'Body', to=['your@email.com'])
        email.send()
        return JsonResponse({'status':True})
    else:
        return render(request,"FAQ.html")

def Support_Sent_Email(request):
    
    email = EmailMessage('Subject', 'Body', to=['your@email.com'])
    email.send()
    return render(request,"FAQ.html")
