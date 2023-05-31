from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Like, Comment, Follow, Otp, Profile
from .sendmail import send_mail
import json
import sys
import os
import random
from datetime import datetime, timezone

root = "/home/clickviral/viral"
# Create your views here.


def feed(request):
    # redirect if user isnt logged in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    return render(request, "posts.html")


def comment(request, query):
    # redirect if user isnt logged in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    if request.method == "POST":
        comment_article = request.POST.get("article").strip()
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

        return JsonResponse(new_comment.to_dict(request.user.id), safe=False)

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

        return JsonResponse({"post": post, "comments": comments})


def edit_post(request, query):
    # redirect if user isnt logged in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    # Handle post request to edit a post
    if request.method == "POST":
        article = request.POST.get("post").strip()

        # Find post from main post or comment
        try:
            post = Post.objects.get(id=query)
        except:
            post = Comment.objects.get(id=query)

        post.article = article
        post.edited_at = datetime.now()
        post.edited = True
        post.save()

        return JsonResponse(json.dumps(post.to_dict(request.user.id)), safe=False)


def profile(request, query):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else:
        try:
            user = User.objects.get(username=query)
            f_count = Follow.objects.filter(user=user).count()
            profile = Profile.objects.get(user=user)
            profile.followers = f_count
            profile.save()
            profile = Profile.objects.get(user=user)
            follow_value = request.user in [
                i.follow for i in Follow.objects.filter(user=user)
            ]
        except:
            return render(request, "nopage.html")
        return render(
            request,
            "profile.html",
            {
                "user": user,
                "follow_value": follow_value,
                "f_count": f_count,
                "profile": profile,
            },
        )

def edit_profile(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            if request.POST.get('username') == request.user.username:
                if request.POST.get('action') == "upload":
                    username = request.POST.get('username')
                    profile = Profile.objects.get(user=request.user)
                    try:
                        os.remove(f"{root}/media/profile/{username}.{profile.image}")
                    except:
                        pass
                    profile.image = str(request.FILES.get('image')).split(".")[1]
                    profile.save()
                    with open(f"{root}/media/profile/{username}.{profile.image}", "wb+") as file:
                        for chunk in request.FILES.get('image').chunks():
                            file.write(chunk)
                    return JsonResponse({"image": f"{username}.{profile.image}"})
                elif request.POST.get('action') == "about":
                    profile = Profile.objects.get(user=request.user)
                    profile.about = request.POST.get('data')
                    profile.save()
                    return JsonResponse({"data": profile.about})
                elif request.POST.get('action') == "birthday":
                    profile = Profile.objects.get(user=request.user)
                    profile.birthday = request.POST.get('birthday')
                    profile.birthyear = request.POST.get('birthyear')
                    profile.save()
                    return JsonResponse({"birthday": profile.birthday, "birthyear": profile.birthyear})
                elif request.POST.get('action') == "gender":
                    profile = Profile.objects.get(user=request.user)
                    profile.gender = request.POST.get('data')
                    profile.save()
                    return JsonResponse({"data": profile.gender})
                elif request.POST.get('action') == "location":
                    profile = Profile.objects.get(user=request.user)
                    profile.location = request.POST.get('data')
                    profile.save()
                    return JsonResponse({"data": profile.location})
                else:
                    return JsonResponse({"image": "empty"})
            else:
                return HttpResponse("...")
        else:
            return HttpResponse("...")


def delete(request, query):
    sys.stderr.write(f"\n{query}\n")
    try:
        post = Post.objects.get(id=query)
    except:
        post = Comment.objects.get(id=query)

    if post.to_dict(request.user.id)["name"] == request.user.username:
        pass
    else:
        return HttpResponse("...")

    if post.media != "empty":
        os.remove(f"{root}/media/posts/{post.id}.{post.media}")
    else:
        pass

    try:
        post = Post.objects.get(id=query).delete()
    except:
        post = Comment.objects.get(id=query).delete()
    return HttpResponse("...")


def follow(request, query):
    try:
        try:
            f_user = User.objects.get(username=query)
            follow = Follow.objects.get(user=f_user, follow=request.user)
            follow.delete()
        except:
            f_user = User.objects.get(username=query)
            profile = Profile.objects.get(user=f_user)
            profile.followers += 1
            profile.save()
            Follow(user=f_user, follow=request.user).save()
    except:
        pass
    f_user = User.objects.get(username=query)
    count = Follow.objects.filter(user=f_user).count()
    return HttpResponse(count)


def fetch_posts(request):
    user = request.user.id
    try:
        posts = Post.objects.all()
        posts = [i.to_dict(user) for i in posts]
        posts.reverse()

    except:
        posts = []

    return JsonResponse(posts, safe=False)

def chat(request, query):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else:
        try:
            user = User.objects.get(username=query)
        except:
            return render(request, "nopage.html")
        return render(
            request,
            "chat.html",
            {
                "tab": user.username,
            },
        )

def get_chats(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else:
        chats = [Chat.objects.filter(sender=self.user).user.username] + [Chat.objects.filter(recipient=query).user.username]
        chats = list(set(chats))

        return JsonResponse(chats, safe=False)

def get_messages(request, query):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else:
        chats = Chat.objects.filter(sender=self.user, recipient=query) + Chat.objects.filter(sender=query, recipient=self.user)
        chats = [i.to_dict() for i in chats]
        chats.reverse()

        return JsonResponse(chats, safe=False)

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
    # Todo

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


def get_post(request, query):
    editable = True
    try:
        post = Post.objects.get(id=query)
    except:
        post = Comment.objects.get(id=query)
    created = post.created_at
    now = datetime.now(timezone.utc)
    diff = now - created
    post = post.to_dict(request.user.id)
    if post["name"] != request.user.username:
        return HttpResponse("Permission Denied", status=403)
    if diff.total_seconds() > 1800:
        editable = False
    post["editable"] = editable
    return JsonResponse([post], safe=False)


def new_post(request):
    if request.method == "POST":
        post_article = request.POST.get("article")
        media = "empty"
        user_id = request.user.id
        try:
            media_file = request.FILES.get("media")
            media = str(media_file).split(".")[1]
            assert media_file is not None
            post = Post(media=media, user_id=user_id, article=post_article)
            with open(f"{root}/media/posts/{post.id}.{media}", "wb+") as file:
                for chunk in media_file.chunks():
                    file.write(chunk)

        except:
            post = Post(media=media, user_id=user_id, article=post_article)

        id = post.id

        post.save()

        return HttpResponse(f"{id}")
    return render(request, "newpost.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"].strip()
        password = request.POST["password"].strip()
        email = request.POST["email"].strip()

        try:
            user = authenticate(request, username=username, password=password)

            assert user is not None

            login(request, user)

            return HttpResponse("0")

        except:
            username = User.objects.get(email__exact=email).username
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                return HttpResponse("0")

            return HttpResponse("1")

    return render(request, "login.html")


def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("feed"))

    return render(request, "register.html")


def logout_view(request):
    logout(request)

    return HttpResponseRedirect(reverse("login"))


def request_code(request):
    if request.method == "POST":
        username = request.POST["username"].strip()
        email = request.POST["email"].strip()

        try:
            try:
                user = User.objects.get(username=username)
                return HttpResponse("1")
            except:
                user = User.objects.get(email=email)
                return HttpResponse("2")
        except:
            pass

        try:
            Otp.objects.get(username=username, mail=email).delete()
        except:
            pass
        otp = str(random.randint(100000, 999999))
        sys.stderr.write(f"{request}\n")
        new_otp = Otp(username=username, mail=email, otp=otp)

        new_otp.save()
        send_mail(
            email,
            f"ClickViral OTP Verification Code For: {username}",
            f"Hello {username},\n\nYour OTP is {otp}\n\nIf You did not request this code, please ignore this email.\n\nClickViral Team",
        )
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

            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email,
            )
            Profile(user=user).save()
            login(request, user)

            Otp.objects.get(username=username, mail=email).delete()

            return HttpResponse("0")
        except:
            try:
                otp = Otp.objects.get(username=username, mail=email)
                otp.tries += 1
                otp.save()
            except:
                pass
            return HttpResponse("1")
