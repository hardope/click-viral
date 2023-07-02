# Description: Comment view
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Comment

root = "/home/clickviral/clickviral"

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
            if comment_article == "":
                return HttpResponse("...")
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