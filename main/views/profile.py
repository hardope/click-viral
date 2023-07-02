# Desc: Profile view
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from ..models import Follow, Profile

def profile(request, query):
    try:
        user = User.objects.get(username=query)
        f_count = Follow.objects.filter(user=user).count()
        profile = Profile.objects.get(user=user)
        profile.followers = f_count
        profile.save()
        profile = Profile.objects.get(user=user)
    except:
        return render(request, "nopage.html")

    if not request.user.is_authenticated:
        return render(
            request,
            "profile_noauth.html",
            {
                "user": user,
                "profile": profile,
                "f_count": f_count,
            },
        )

    else:
        follow_value = request.user in [
            i.follow for i in Follow.objects.filter(user=user)
        ]
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
