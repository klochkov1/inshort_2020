from django.urls import path

from . import views

urlpatterns = [
    path('url/<int:custom_url_id>/', views.detail),
    path('url/<int:custom_url_id>/history/', views.history),
    path('<str:requested_url>', views.redirect)
]
