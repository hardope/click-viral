from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

def feed(request):
    # redirect if user isnt logged in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    return render(request, "posts.html")