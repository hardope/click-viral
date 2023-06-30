# Description: View for the feed page
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from .fetch_posts import collect_personalized_posts

def feed(request):
    # redirect if user isnt logged in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    return render(request, "posts.html")

def fetch_posts(request):
    posts = collect_personalized_posts(request.user)
    posts = [i.to_dict(request.user) for i in posts]

    return JsonResponse(posts, safe=False)