# Desc: View for editing posts
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.db.models import Q
from ..models import Post, Comment

from datetime import datetime, timezone

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

        if post.user_id != request.user.id:
            return HttpResponse("...")

        created = post.created_at
        now = datetime.now(timezone.utc)
        diff = now - created

        if diff.total_seconds() > 43200:
            return HttpResponse("...")


        post.article = article
        post.edited_at = datetime.now()
        post.edited = True
        post.save()

        return JsonResponse(json.dumps(post.to_dict(request.user.id)), safe=False)
