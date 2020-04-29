from django.urls import path, include
from . import views

base_urls = [
    path('add', views.add_url, name="add_url"),
    path('<slug:short_url>/delete', views.delete_url, name="delete"),
    path('my', views.user_urls, name="user_urls"),
    path('generate', views.get_new_shortin, name="generate")
]

urlpatterns = [
    path('urls/', include(base_urls)),
    # main functionality, custom urls rediraction
    path('<slug:requested_url>', views.redirect, name="redirection_url")
]