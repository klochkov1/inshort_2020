from django.urls import path

from . import views

urlpatterns = [
<<<<<<< HEAD
    path('urls/<int:short_url>/', views.detail, name="detail"),
    path('urls/<int:short_url>/history/', views.history, name="url_history"),
    path('urls/add', views.add_url, name="add_url"),
    path('urls/add_url_from', views.add_url_form, name="add_url_form"),
    path('users/<str:user>/urls', views.user_urls, name="user_urls"),
=======
    path('urls/<int:short_url>/', views.detail),
    path('urls/<int:short_url>/history/', views.history),
    path('users/<str:user>/urls', views.user_urls),
>>>>>>> klochkov
    # main functionality, custom urls rediraction
    path('<slug:requested_url>', views.redirect)
]
