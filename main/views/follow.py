# Description: View for follow
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Follow

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