from django.urls import path

from . import views

urlpatterns = [
    path('urls/add', views.add_url, name="add_url"),
    path('urls/<slug:short_url>/delete', views.delete_url, name="delete"),
    path('urls/<slug:short_url>/history', views.history, name="url_history"),
    path('urls/add_url_form', views.add_url_form, name="add_url_form"),
    path('users/<slug:user>/urls', views.user_urls, name="user_urls"),
    # main functionality, custom urls rediraction
    path('<slug:requested_url>', views.redirect, name="redirection_url")
]
