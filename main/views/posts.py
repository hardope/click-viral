#Description: Views for posts
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Post, Like, Comment
from datetime import datetime, timezone

root = "/home/ubuntu/viral"

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
        try:
            post = Comment.objects.get(id=query)
        except:
            return HttpResponse("...")
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
            if post_article == "":
                return HttpResponse("...")

        id = post.id

        post.save()

        return HttpResponse(f"{id}")
    return render(request, "newpost.html")


def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("feed"))
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
            if email == "":
                return HttpResponse("1")

            try:
                username = User.objects.get(email__exact=email).username
                user = authenticate(request, username=username, password=password)

                if user is not None:
                    login(request, user)

                    return HttpResponse("0")
                return HttpResponse("1")
            except:
                pass

            return HttpResponse("1")

    return render(request, "login.html")

