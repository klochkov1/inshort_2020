from django.contrib.auth import views
from django.urls import path
from accounts.views import LoginView, RegisterView, logout_user
 
urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path('register/', RegisterView.as_view(), name="register"),
    path('logout/', logout_user, name="logout")]