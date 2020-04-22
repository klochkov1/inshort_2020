from django.urls import path

from . import views

urlpatterns = [
    path('urls/<int:short_url>/', views.detail),
    path('urls/<int:short_url>/history/', views.history),
    path('users/<str:user>/urls', views.user_urls),
    # main functionality, custom urls rediraction
    path('<slug:requested_url>', views.redirect)
]
