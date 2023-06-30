from django.urls import path

from . import views

urlpatterns = [
    # Main Views
    path("", views.feed, name="feed"),
   
    path("login", views.login_view, name="login"),
]
