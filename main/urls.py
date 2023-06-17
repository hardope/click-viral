from django.urls import path

from . import views

urlpatterns = [
    # Main Views
    path("", views.feed, name="feed"),
    path("chat/<query>", views.chat, name="chat"),
    path("profile/<query>", views.profile, name="profile"),
    path("security", views.security, name="security"),
    path("forgot_password", views.forgot_password, name="forgot_password"),

    # Json Views
    path("request_code", views.request_code, name="request_code"),
    path("check_otp", views.check_otp, name="check_otp"),
    path("notification", views.notification, name="notification"),
    path("like/<query>", views.like, name="like"),
    path("unlike/<query>", views.unlike, name="unlike"),
    path("fetch_posts", views.fetch_posts, name="fetch_posts"),
    path("get_post/<query>", views.get_post, name="get_post"),
    path("view_likes/<query>", views.view_likes, name="view_likes"),
    path("follow/<query>", views.follow, name="follow"),
    path("new_post", views.new_post, name="new_post"),
    path("comment/<query>", views.comment, name="comment"),
    path("edit_post/<query>", views.edit_post, name="edit_post"),
    path("delete/<query>", views.delete, name="delete"),
    path("edit_profile", views.edit_profile, name="edit_profile"),
    path("get_chats", views.get_chats, name="get_chats"),
    path("get_messages/<query>", views.get_messages, name="get_messages"),
    path("send_message", views.send_message, name="send_message"),
    path("search", views.search, name="search"),

    # Auth Views
    path("login", views.login_view, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.logout_view, name="logout"),
]
