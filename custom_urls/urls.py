from django.urls import path, include
from . import views

base_urls = [
    path('add', views.add_url, name="add_url"),
    path('<slug:short_url>/delete', views.delete_url, name="delete"),
    path('<slug:short_url>/history', views.history, name="url_history"),
    path('add_url_form', views.add_url_form, name="add_url_form"),
    path('my', views.user_urls, name="user_urls"),
]

urlpatterns = [
    path('urls/', include(base_urls)),
    # main functionality, custom urls rediraction
    path('<slug:requested_url>', views.redirect, name="redirection_url")
]