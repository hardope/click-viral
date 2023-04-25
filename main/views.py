from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Like, Comment, Follow, Otp
import json
import sys
import os
import random
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
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else:
        try:
            sys.stderr.write("Here")
            user = User.objects.get(username=query)
            try:
                f_count = Follow.objects.filter(user=user).count()
            except:
                f_count = 0
            user.profile.followers = f_count
            sys.stderr.write("01")
            user.profile.save()
            user = User.objects.get(username=query)
            follow_value = request.user in [
                i.follow for i in Follow.objects.filter(user=user)
            ]
        except:
            sys.stderr.write(f"Error\n")
            return render(request, "nopage.html")
        sys.stderr.write(f"{user.profile.image}, {user.profile.gender}\n")
        return render(
            request,
            "profile.html",
            {"user": user, "follow_value": follow_value, "f_count": f_count},
        )


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
            f_user = User.objects.get(username=query)
            follow = Follow.objects.get(user=f_user, follow=request.user)
            follow.delete()
        except:
            user = User.objects.get(username=query)
            user.profile.followers += 1
            user.save()
            Follow(user=user, follow=request.user).save()
    except:
        pass
    f_user = User.objects.get(username=query)
    count = Follow.objects.filter(user=f_user).count()
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

def request_code(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        try:
            try:
                user = User.objects.get(username=username)
                return HttpResponse("1")
            except:
                user = User.objects.get(email=email)
                return HttpResponse("2")
        except:
            pass
        
        otp = str(random.randint(100000, 999999))
        sys.stderr.write(f"{request}\n")
        new_otp = Otp(username=username, mail=email, otp=otp)

        new_otp.save()
        return HttpResponse("0")

def check_otp(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        otp = request.POST["otp"]

        try:
            otp = Otp.objects.get(username=username, otp=otp, mail=email)

            if otp.tries > 10:
                return HttpResponse("2")
            
            created = otp.created_at
            now = datetime.now(timezone.utc)
            diff = now - created

            if diff.total_seconds() > 43200:
                return HttpResponse("2")

            user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name, email=email)
            login(request, user)

            return HttpResponse("0")
        except:
            try:
                otp = Otp.objects.get(username=username, mail=email)
                otp.tries += 1
                otp.save()
            except:
                pass
            return HttpResponse("1")

        
