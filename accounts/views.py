from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views.generic import TemplateView
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.models import User
from custom_urls.models import CustomUrl


class LoginView(TemplateView):
    template_name = "registration/login.html"

    def dispatch(self, request, *args, **kwargs):
        context = {}
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse("home"))
            else:
                context['error'] = "Логин или пароль неправильные"
        return render(request, self.template_name, context)


class RegisterView(TemplateView):
    template_name = "registration/register.html"

    def dispatch(self, request, *args, **kwargs):
        context = {}
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            password2 = request.POST.get('password2')
            if User.objects.filter(username=username).exists():
               context['error'] = "Таке ім'я вже існує"
            elif password == password2:
                new_user = User.objects.create_user(username, email, password)
                # Assing anonymus session urls to registerd user
                urls = CustomUrl.objects.filter(session__pk=request.session.session_key)
                for u in urls:
                    u.owner = new_user
                    u.save()       
                return redirect(reverse("home"))
        return render(request, self.template_name, context)

def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))
