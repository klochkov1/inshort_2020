from django.shortcuts import render
from django.core.mail import EmailMessage
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

from django.http import HttpResponse


def index(request):
    return render(request, "index.html")

@csrf_exempt
def FAQ(request):
    if request.method == 'POST':
        body_messege = json.loads(request.body).get('message', '')
        email = EmailMessage('Support_Messege', body_messege, to=['amurahovskiy@gmail.com'])
        email.send()
        return JsonResponse({'status':True})
    else:
        return render(request,"FAQ.html")

