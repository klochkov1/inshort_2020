from django.contrib.auth import views
from django.urls import path, include
from accounts.views import LoginView, RegisterView
 
urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path('register/', RegisterView.as_view(), name="register"),
    path('social-auth/', include('social_django.urls', namespace="social")),
    #social-auth/ i am not shure, but this for creating parth in login.html
    ]