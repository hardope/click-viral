from django.urls import path

from . import views

urlpatterns = [
    # Main Views
    path("", views.feed, name="feed"),
    path("fetch_posts", views.fetch_posts, name="fetch_posts"),

   
    path("login", views.login_view, name="login"),
]
