from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Like, Comment, Follow
import json
import sys
import os
from datetime import datetime, timezone

root = "/home/clickviral/viral"
# Create your views here.


def feed(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    user = request.user.id
    try:
        posts = Post.objects.all()
        posts = [i.to_dict(user) for i in posts]
        posts.reverse()

    except:
        posts = []

    return render(
        request, "posts.html", {"username": request.user.username, "posts": posts}
    )


def comment(request, query):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    if request.method == "POST":
        comment_article = request.POST.get("comment")
        media = "empty"
        user_id = request.user.id
        try:
            media_file = request.FILES["media"]
            media = str(media_file).split(".")[1]

            assert media_file is not None
            try:
                update = Post.objects.get(id=query)
                update.comments += 1
                update.save()

                new_comment = Comment(
                    media=media, user_id=user_id, article=comment_article, post_id=query
                )
            except:
                update = Comment.objects.get(id=query)
                update.comments += 1
                update.save()

                new_comment = Comment(
                    media=media,
                    user_id=user_id,
                    article=comment_article,
                    m_comment_id=query,
                )

            with open(f"{root}/media/posts/{new_comment.id}.{media}", "wb+") as file:
                for chunk in media_file.chunks():
                    file.write(chunk)

        except:
            try:
                update = Post.objects.get(id=query)
                update.comments += 1
                update.save()

                new_comment = Comment(
                    media=media, user_id=user_id, article=comment_article, post_id=query
                )
            except:
                update = Comment.objects.get(id=query)
                update.comments += 1
                update.save()

                new_comment = Comment(
                    media=media,
                    user_id=user_id,
                    article=comment_article,
                    m_comment_id=query,
                )

        new_comment.save()

        return HttpResponseRedirect(f"{query}")

    else:
        try:
            post = Post.objects.get(id=query).to_dict(request.user.id)
        except:
            post = Comment.objects.get(id=query).to_dict(request.user.id)

        comments = Comment.objects.filter(post_id=query)
        comments1 = Comment.objects.filter(m_comment_id=query)

        comments = [i.to_dict(request.user.id) for i in comments] + [
            i.to_dict(request.user.id) for i in comments1
        ]

        return render(request, "comment.html", {"post": post, "comments": comments})


def edit_post(request, query):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    if request.method == "POST":
        article = request.POST.get("post").strip()

        try:
            post = Post.objects.get(id=query)
        except:
            post = Comment.objects.get(id=query)

        post.article = article
        post.edited_at = datetime.now()
        post.edited = True
        post.save()
        pid = query

        return redirect(f"/comment/{pid}")

    else:
        pid = query
        editable = True
        try:
            post = Post.objects.get(id=query)
        except:
            post = Comment.objects.get(id=query)
        created = post.created_at
        now = datetime.now(timezone.utc)
        diff = now - created
        post = post.to_dict(request.user.id)
        if post["name"] != request.user:
            return redirect("/comment/{pid}")
        if diff.total_seconds() > 1800:
            editable = False

        return render(request, "edit_post.html", {"post": post, "editable": editable})


def profile(request, query):
    try:
        user = User.objects.get(username=query)
        user.followers = Follow.objects.filter(user=user).count()
        user.save()
        user = User.objects.get(username=query)
        follow_value = request.user in Follow.objects.filter(user=user).values_list("follow", flat=True)
    except:
        return render(request, "nopage.html")

    return render(request, "profile.html", {"user": user, "follow_value": follow_value})


def delete(request, query):
    try:
        post = Post.objects.get(id=query)
    except:
        post = Comment.objects.get(id=query)
    if post.media != "empty":
        os.remove(f"/home/clickviral/viral/media/posts/{post.id}.{post.media}")
    else:
        pass
    try:
        post = Post.objects.get(id=query).delete()
    except:
        post = Comment.objects.get(id=query).delete()
    return redirect("/")

def follow(request, query):
    try:
        try:
            follow = Follow.objects.get(user=query, follow=request.user)
            follow.delete()
        except:
            user = User.objects.get(username=query)
            user.profile.followers += 1
            user.save()
            Follow(user=user, follow=request.user).save()
    except:
        pass
    count = Follow.objects.filter(user=query)
    count = len(str(i) for i in count)
    return HttpResponse(count)


def fetch_posts(request):
    posts = Post.objects.all()
    posts = [i.to_dict() for i in posts]

    return JsonResponse(posts, safe=False)


def view_likes(request, query):
    try:
        try:
            list_likes = Like.objects.all().filter(post_id=query)
        except:
            list_likes = Like.objects.all().filter(comment_id=query)
        names = [i.name_user() for i in list_likes]
    except:
        names = []

    return HttpResponse(json.dumps(names))


def notification(request):
    return HttpResponse(json.dumps([]))


def like(request, query):
    id = request.user.id
    try:
        try:
            Like.objects.get(user_id=id, post_id=query)
        except:
            Like.objects.get(user_id=id, comment_id=query)
    except:
        try:
            update_post = Post.objects.get(id=query)
            update_post.likes += 1
            update_post.save()

            new_like = Like(post_id=query, user_id=id)
        except:
            update_post = Comment.objects.get(id=query)
            update_post.likes += 1
            update_post.save()

            new_like = Like(comment_id=query, user_id=id)

        new_like.save()

    return HttpResponse(json.dumps([]))


def unlike(request, query):
    id = request.user.id

    try:
        update_post = Post.objects.get(id=query)
        update_post.likes -= 1
        update_post.save()
        Like.objects.get(user_id=id, post_id=query).delete()
    except:
        update_post = Comment.objects.get(id=query)
        update_post.likes -= 1
        update_post.save()
        Like.objects.get(user_id=id, comment_id=query).delete()

    return HttpResponse("")


def new_post(request):
    if request.method == "POST":
        post_article = request.POST.get("post")
        media = "empty"
        user_id = request.user.id
        try:
            media_file = request.FILES["media"]
            media = str(media_file).split(".")[1]

            assert media_file is not None

            post = Post(media=media, user_id=user_id, article=post_article)

            with open(f"{root}/media/posts/{post.id}.{media}", "wb+") as file:
                for chunk in media_file.chunks():
                    file.write(chunk)

        except:
            post = Post(media=media, user_id=user_id, article=post_article)

        post.save()

        return HttpResponseRedirect(reverse("feed"))
    return render(request, "newpost.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            return HttpResponseRedirect(reverse("feed"))

        return render(request, "login.html", {"message": "Invalid Credentials"})

    return render(request, "login.html")


def register(request):
    if request.method == "POST":
        username = request.POST.get("username").strip()
        password = request.POST.get("password")
        confirm = request.POST.get("confirm")

        if confirm != password:
            return render(request, "register.html", {"message": "Invalid Credentials"})

        if confirm != password:
            return render(request, "register.html", {"message": "Invalid Credentials"})

        if " " in username:
            return render(
                request, "register.html", {"message": "Username cannot contain spaces"}
            )

        try:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect(reverse("feed"))

        except:
            return render(request, "register.html", {"message": "Username Taken"})

    return render(request, "register.html")


def logout_view(request):
    logout(request)

    return HttpResponseRedirect(reverse("login"))
