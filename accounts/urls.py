from django.contrib.auth import views
from django.urls import path
from accounts.views import LoginView, RegisterView, logout_user, include

urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path('register/', RegisterView.as_view(), name="register"),
    path('logout/', logout_user, name="logout"),
    path('social-auth/', include('social_django.urls', namespace="social")),
    # social-auth/ i am not shure, but this for creating parth in login.html
]
